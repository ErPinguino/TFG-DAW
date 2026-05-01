from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel
from typing import List
from Models.game import GameResponse

class CartORM(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True) 
    
    items = relationship("CartItemORM", back_populates="cart", cascade="all, delete-orphan")

class CartItemORM(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    quantity = Column(Integer, default=1)

    cart = relationship("CartORM", back_populates="items")
    game = relationship("GameORM") 

class CartItemBase(BaseModel):
    game_id: int
    quantity: int = 1

class CartItemResponse(CartItemBase):
    id: int
    game: GameResponse 

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    id: int
    user_id: int
    items: List[CartItemResponse] = []
    total_price: float = 0.0

    class Config:
        from_attributes = True