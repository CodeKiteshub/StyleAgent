"""
Image analysis model for StyleAgent computer vision results
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Float, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base
import uuid


class ImageAnalysis(Base):
    """Image analysis model for storing computer vision results"""
    
    __tablename__ = "image_analyses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=True)
    
    # Image information
    original_filename = Column(String, nullable=True)
    image_url = Column(String, nullable=False)  # S3 or storage URL
    image_size = Column(Integer, nullable=True)  # File size in bytes
    image_dimensions = Column(JSON, nullable=True)  # {"width": 1920, "height": 1080}
    
    # Computer vision analysis results
    body_pose_data = Column(JSON, nullable=True)  # OpenPose results
    body_type_prediction = Column(String, nullable=True)  # Predicted body type
    body_measurements = Column(JSON, nullable=True)  # Estimated measurements
    
    # Clothing detection
    detected_clothing = Column(JSON, default=list)  # Array of detected clothing items
    clothing_colors = Column(JSON, default=list)  # Detected colors in clothing
    clothing_style = Column(String, nullable=True)  # Overall style classification
    
    # CLIP-ViT analysis
    style_embeddings = Column(JSON, nullable=True)  # Style feature embeddings
    style_attributes = Column(JSON, default=dict)  # Detected style attributes
    
    # Trend analysis
    trend_elements = Column(JSON, default=list)  # Trendy elements detected
    social_media_score = Column(Float, default=0.0)  # Social media potential score
    viral_potential = Column(Float, default=0.0)  # Viral potential score
    
    # Quality metrics
    image_quality_score = Column(Float, nullable=True)  # Image quality assessment
    analysis_confidence = Column(Float, nullable=True)  # Overall confidence in analysis
    
    # Processing status
    processing_status = Column(String, default="pending")  # pending, processing, completed, failed
    error_message = Column(Text, nullable=True)  # Error message if processing failed
    
    # Processing times
    processing_started_at = Column(DateTime(timezone=True), nullable=True)
    processing_completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="image_analyses")
    conversation = relationship("Conversation")
    
    def __repr__(self):
        return f"<ImageAnalysis(id={self.id}, user_id={self.user_id}, status={self.processing_status})>"
    
    def to_dict(self):
        """Convert image analysis to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "conversation_id": self.conversation_id,
            "original_filename": self.original_filename,
            "image_url": self.image_url,
            "image_size": self.image_size,
            "image_dimensions": self.image_dimensions,
            "body_pose_data": self.body_pose_data,
            "body_type_prediction": self.body_type_prediction,
            "body_measurements": self.body_measurements,
            "detected_clothing": self.detected_clothing,
            "clothing_colors": self.clothing_colors,
            "clothing_style": self.clothing_style,
            "style_embeddings": self.style_embeddings,
            "style_attributes": self.style_attributes,
            "trend_elements": self.trend_elements,
            "social_media_score": self.social_media_score,
            "viral_potential": self.viral_potential,
            "image_quality_score": self.image_quality_score,
            "analysis_confidence": self.analysis_confidence,
            "processing_status": self.processing_status,
            "error_message": self.error_message,
            "processing_started_at": self.processing_started_at.isoformat() if self.processing_started_at else None,
            "processing_completed_at": self.processing_completed_at.isoformat() if self.processing_completed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class TrendAnalysis(Base):
    """Trend analysis results from social media"""
    
    __tablename__ = "trend_analyses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Trend information
    trend_name = Column(String, nullable=False)
    trend_category = Column(String, nullable=True)  # e.g., "color", "style", "item"
    description = Column(Text, nullable=True)
    
    # Social media metrics
    instagram_mentions = Column(Integer, default=0)
    tiktok_mentions = Column(Integer, default=0)
    twitter_mentions = Column(Integer, default=0)
    
    # Trend scoring
    popularity_score = Column(Float, default=0.0)  # 0-100 popularity score
    growth_rate = Column(Float, default=0.0)  # Growth rate percentage
    viral_coefficient = Column(Float, default=0.0)  # Viral potential
    
    # Associated keywords and hashtags
    keywords = Column(JSON, default=list)
    hashtags = Column(JSON, default=list)
    
    # Temporal data
    peak_date = Column(DateTime(timezone=True), nullable=True)
    trend_duration_days = Column(Integer, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<TrendAnalysis(id={self.id}, trend_name={self.trend_name})>"
    
    def to_dict(self):
        """Convert trend analysis to dictionary"""
        return {
            "id": self.id,
            "trend_name": self.trend_name,
            "trend_category": self.trend_category,
            "description": self.description,
            "instagram_mentions": self.instagram_mentions,
            "tiktok_mentions": self.tiktok_mentions,
            "twitter_mentions": self.twitter_mentions,
            "popularity_score": self.popularity_score,
            "growth_rate": self.growth_rate,
            "viral_coefficient": self.viral_coefficient,
            "keywords": self.keywords,
            "hashtags": self.hashtags,
            "peak_date": self.peak_date.isoformat() if self.peak_date else None,
            "trend_duration_days": self.trend_duration_days,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }