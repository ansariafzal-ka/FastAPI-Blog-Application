from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime
from src.configs.db import Base
from datetime import datetime

class UserModel(Base):
    __tablename__='user'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    hash_password = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserSchema(BaseModel):
    user_name: str = Field(..., min_length=1)
    email: str = Field(...)
    password: str = Field(..., min_length=1)

class UserOutSchema(BaseModel):
    id: int = Field(..., gt=0)
    user_name: str = Field(..., min_length=1)
    email: str = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

class LoginSchema(BaseModel):
    user_name: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)