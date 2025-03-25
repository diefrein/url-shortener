from sqlalchemy import Column, UUID, String, TIMESTAMP, Integer
from sqlalchemy.ext.declarative import declarative_base
import uuid
from pydantic import BaseModel, Field
from uuid import UUID as UUID_BASE
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID, primary_key=True, default=lambda: uuid.uuid4(), nullable=False)
    name = Column(String, nullable=False)
    
class UserCreate(BaseModel):
    name: str = Field(None)
    
class Url(Base):
    __tablename__ = 'urls'
    id = Column(UUID, primary_key=True, default=lambda: uuid.uuid4(), nullable=False)
    full_url = Column(String, nullable=False)
    short_url = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False)
    latest_used_at = Column(TIMESTAMP(timezone=False), nullable=True)
    times_used = Column(Integer, nullable=False, default=0)
    expires_at = Column(TIMESTAMP(timezone=False), nullable=True)
    
class UrlCreate(BaseModel):
    full_url: str = Field(None)
    user_id: UUID_BASE = Field(None)
    expires_at: datetime = Field(None)