from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone
from pydantic import BaseModel, model_validator 
from typing import List, Optional

class OrderORM(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String, default="completed") # completed, pending, cancelled

    user = relationship("UserORM")
    items = relationship("OrderItemORM", back_populates="order")

class OrderItemORM(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Float, nullable=False) 

    order = relationship("OrderORM", back_populates="items")
    game = relationship("GameORM")

class OrderItemResponse(BaseModel):
    game_id: int
    quantity: int
    price_at_purchase: float
    game_title: Optional[str] = None 

    @model_validator(mode='before') 
    @classmethod
    def get_title_from_relationship(cls, data):
        # Verificamos si tiene la relación 'game' cargada
        if hasattr(data, "game") and data.game:
            setattr(data, "game_title", data.game.title)
        return data

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    created_at: datetime
    status: str
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True 