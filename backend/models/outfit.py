"""
Outfit model for StyleAgent recommendations
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Float, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base
import uuid


class Outfit(Base):
    """Outfit model for storing outfit recommendations"""
    
    __tablename__ = "outfits"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Basic outfit information
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=False)
    
    # Style attributes
    style_category = Column(String, nullable=True)  # e.g., "casual", "formal", "streetwear"
    occasion = Column(String, nullable=True)  # e.g., "work", "date", "party"
    season = Column(String, nullable=True)  # e.g., "spring", "summer", "fall", "winter"
    
    # Clothing items (stored as JSON array)
    clothing_items = Column(JSON, default=list)  # Array of clothing item objects
    
    # Pricing information
    price_range = Column(String, nullable=True)  # e.g., "$100-200"
    min_price = Column(Float, nullable=True)
    max_price = Column(Float, nullable=True)
    
    # Body type compatibility
    body_types = Column(JSON, default=list)  # Array of compatible body types
    
    # Color information
    primary_colors = Column(JSON, default=list)  # Array of primary colors
    color_palette = Column(JSON, default=dict)  # Color palette information
    
    # Social media and trend data
    hashtags = Column(JSON, default=list)  # Array of hashtags
    trend_score = Column(Float, default=0.0)  # Trend score (0-100)
    social_stats = Column(JSON, default=dict)  # Likes, shares, etc.
    
    # Vector embeddings for similarity search
    embedding = Column(JSON, nullable=True)  # Store embedding as JSON array
    
    # Metadata
    source = Column(String, nullable=True)  # Source of the outfit (e.g., "pinterest", "instagram")
    tags = Column(JSON, default=list)  # Additional tags
    
    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Outfit(id={self.id}, title={self.title})>"
    
    def to_dict(self):
        """Convert outfit to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "image_url": self.image_url,
            "style_category": self.style_category,
            "occasion": self.occasion,
            "season": self.season,
            "clothing_items": self.clothing_items,
            "price_range": self.price_range,
            "min_price": self.min_price,
            "max_price": self.max_price,
            "body_types": self.body_types,
            "primary_colors": self.primary_colors,
            "color_palette": self.color_palette,
            "hashtags": self.hashtags,
            "trend_score": self.trend_score,
            "social_stats": self.social_stats,
            "source": self.source,
            "tags": self.tags,
            "is_active": self.is_active,
            "is_featured": self.is_featured,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class OutfitRecommendation(Base):
    """Outfit recommendations generated for users"""
    
    __tablename__ = "outfit_recommendations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=True)
    outfit_id = Column(String, ForeignKey("outfits.id"), nullable=False)
    
    # Recommendation metadata
    relevance_score = Column(Float, nullable=False)  # How relevant this outfit is to the user
    body_fit_percentage = Column(Float, nullable=True)  # Body fit match percentage
    style_match_score = Column(Float, nullable=True)  # Style preference match
    
    # Generated content for this recommendation
    generated_caption = Column(Text, nullable=True)  # AI-generated caption
    generated_hashtags = Column(JSON, default=list)  # AI-generated hashtags
    
    # User interaction
    is_liked = Column(Boolean, default=False)
    is_saved = Column(Boolean, default=False)
    is_shared = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    conversation = relationship("Conversation")
    outfit = relationship("Outfit")
    
    def __repr__(self):
        return f"<OutfitRecommendation(id={self.id}, user_id={self.user_id}, outfit_id={self.outfit_id})>"
    
    def to_dict(self):
        """Convert recommendation to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "conversation_id": self.conversation_id,
            "outfit_id": self.outfit_id,
            "relevance_score": self.relevance_score,
            "body_fit_percentage": self.body_fit_percentage,
            "style_match_score": self.style_match_score,
            "generated_caption": self.generated_caption,
            "generated_hashtags": self.generated_hashtags,
            "is_liked": self.is_liked,
            "is_saved": self.is_saved,
            "is_shared": self.is_shared,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }