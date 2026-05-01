from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, relationship
from pydantic import BaseModel, Field, conint
from typing import Optional
from database import Base
#Parte ORM

class GameORM(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), unique=True, index=True, nullable=False)
    genre = Column(String(50), index=True, nullable=False)
    platform = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    release_year = Column(Integer, nullable=True)
    multiplayer = Column(Boolean, default=False)
    stock = Column(Integer, default=0, nullable=False)

    def __repr__(self):
        return f"<Game(title={self.title}, genre={self.genre}, platform={self.platform}, price={self.price}, release_year={self.release_year}, multiplayer={self.multiplayer})>"

#Parte Pydantic

#Input DTO

class GameBase(BaseModel):
    title: str = Field(..., max_length=100, description="Title of the game")
    genre: str = Field(..., max_length=50, description="Genre of the game")
    platform: str = Field(..., description="Platform of the game")
    price : float = Field(..., gt=0, description="Price of the game")
    release_year: Optional[conint(ge=1970, lt=2100)] = None
    multiplayer: bool = False
    stock: Optional[conint(ge=0, lt=100)] = None

#Output DTO

class GameResponse(GameBase):
    id: int

    stock: int

    class Config:
        from_attributes = True

#Patch DTO

class GameUpate(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    platform: Optional[str] = None
    price : Optional[float] = None
    release_year: Optional[conint(ge=1970, lt=2100)] = None
    multiplayer: Optional[bool] = None
    stock: Optional[conint(ge=0, lt=100)] = None

    class Config:
        from_attributes = True
