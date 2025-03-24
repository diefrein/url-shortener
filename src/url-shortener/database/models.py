from sqlalchemy import Column, UUID, String
from sqlalchemy.ext.declarative import declarative_base
import uuid
from pydantic import BaseModel, Field
from uuid import UUID as UUID_BASE

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
    
class UrlCreate(BaseModel):
    full_url: str = Field(None)
    user_id: UUID_BASE = Field(None)