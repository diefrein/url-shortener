from sqlalchemy import Column, UUID, String
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID, primary_key=True, default=lambda: uuid.uuid4(), nullable=False)
    name = Column(String, nullable=False)
    
class UserCreate:
    def __init__(self, name: str):
        self.name = name
    
class Url(Base):
    __tablename__ = 'urls'
    id = Column(UUID, primary_key=True, default=lambda: uuid.uuid4(), nullable=False)
    full_url = Column(String, nullable=False)
    short_url = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    
class UrlCreate:
     def __init__(self, full_url: str, short_url: str, user_id: uuid):
        self.full_url = full_url
        self.short_url = short_url
        self.user_id = user_id