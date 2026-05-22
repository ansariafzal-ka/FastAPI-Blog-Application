from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey
from src.configs.db import Base
from typing import Optional
from datetime import datetime
import enum

class BlogCategory(enum.Enum):
    Food = 'Food'
    Tech = 'Tech'
    Fashion = 'Fashion'

class BlogModel(Base):
    __tablename__='blog'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(Enum(BlogCategory), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class BlogSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    category: BlogCategory

class BlogOutSchema(BaseModel):
    id: int = Field(..., gt=0)
    user_id: int = Field(..., gt=0)
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    category: BlogCategory
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)
