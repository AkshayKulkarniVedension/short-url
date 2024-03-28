from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    short_url = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('users.id'))
    click_count = Column(BigInteger, default=0) 

    owner = relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
