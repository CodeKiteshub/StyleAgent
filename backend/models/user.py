"""
User model for StyleAgent
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base
import uuid


class User(Base):
    """User model for storing user profiles and preferences"""
    
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=True)
    username = Column(String, unique=True, index=True, nullable=True)
    
    # User preferences
    style_preferences = Column(JSON, default=dict)  # Store style preferences as JSON
    body_type = Column(String, nullable=True)
    preferred_colors = Column(JSON, default=list)  # Array of preferred colors
    budget_range = Column(String, nullable=True)  # e.g., "$100-200", "$200-500"
    
    # Profile information
    age_range = Column(String, nullable=True)  # e.g., "18-25", "26-35"
    gender = Column(String, nullable=True)
    location = Column(String, nullable=True)
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    image_analyses = relationship("ImageAnalysis", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "style_preferences": self.style_preferences,
            "body_type": self.body_type,
            "preferred_colors": self.preferred_colors,
            "budget_range": self.budget_range,
            "age_range": self.age_range,
            "gender": self.gender,
            "location": self.location,
            "is_active": self.is_active,
            "is_premium": self.is_premium,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }