# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String)
    is_active = Column(Boolean, default=True)
    paddle_customer_id = Column(String, unique=True, nullable=True)
    paddle_subscription_id = Column(String, unique=True, nullable=True)
    is_subscribed = Column(Boolean, default=False)
    subscription_plan = Column(String, default='free')
    subscription_end_date = Column(DateTime, nullable=True)
    oauth_tokens = relationship("OAuthToken", back_populates="user")

class OAuthToken(Base):
    __tablename__ = "token"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    provider = Column(String)
    access_token = Column(String)
    refresh_token = Column(String, nullable=True)
    expires_at = Column(DateTime)
    user = relationship("User", back_populates="oauth_tokens")