from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, relationship
from pydantic import BaseModel, Field, conint, EmailStr
from typing import Optional
from database import Base

#ORM part
class UserORM(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    username = Column(String(50), index = True, unique = True, nullable = False)
    email = Column(String(100), index = True, unique = True, nullable = False)
    hashed_password = Column(String(255), nullable = False)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

#Pydantic part

#Input DTO
class UserBase(BaseModel):
    username: str = Field(..., max_length=50, description="Username of the user")
    email: EmailStr = Field(..., max_length=100, description="Email of the user")
    password: str = Field(..., min_length=8, description="Password of the user")

#Output DTO without password
class UserPublicResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

#Output DTO
class UserResponse(UserPublicResponse):
    id: int

    class Config:
        from_attributes = True

#Patch DTO
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, description="New password")

    class Config:
        from_attributes = True


