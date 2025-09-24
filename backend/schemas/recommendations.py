"""
Pydantic schemas for outfit recommendations and RAG pipeline
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class OutfitCategory(str, Enum):
    """Outfit category enumeration"""
    CASUAL = "casual"
    BUSINESS = "business"
    FORMAL = "formal"
    PARTY = "party"
    DATE = "date"
    WORKOUT = "workout"
    VACATION = "vacation"
    SEASONAL = "seasonal"


class Season(str, Enum):
    """Season enumeration"""
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"
    WINTER = "winter"
    ALL_SEASON = "all_season"


class BodyType(str, Enum):
    """Body type enumeration"""
    PEAR = "pear"
    APPLE = "apple"
    HOURGLASS = "hourglass"
    RECTANGLE = "rectangle"
    INVERTED_TRIANGLE = "inverted_triangle"


class OutfitItem(BaseModel):
    """Individual clothing item in an outfit"""
    category: str = Field(..., description="Clothing category (e.g., shirt, pants)")
    brand: Optional[str] = Field(None, description="Brand name")
    color: str = Field(..., description="Primary color")
    size_range: List[str] = Field(default=[], description="Available sizes")
    price: Optional[float] = Field(None, description="Item price")
    url: Optional[HttpUrl] = Field(None, description="Purchase URL")


class OutfitRecommendation(BaseModel):
    """Outfit recommendation response"""
    outfit_id: str = Field(..., description="Unique outfit ID")
    title: str = Field(..., description="Outfit title")
    description: str = Field(..., description="Outfit description")
    image_url: HttpUrl = Field(..., description="Outfit image URL")
    
    # Style attributes
    category: OutfitCategory = Field(..., description="Outfit category")
    occasion: str = Field(..., description="Suitable occasion")
    season: Season = Field(..., description="Suitable season")
    style_tags: List[str] = Field(default=[], description="Style tags")
    
    # Clothing items
    items: List[OutfitItem] = Field(..., description="Clothing items in the outfit")
    
    # Pricing
    total_price: Optional[float] = Field(None, description="Total outfit price")
    price_range: str = Field(..., description="Price range category")
    
    # Body compatibility
    body_types: List[BodyType] = Field(..., description="Compatible body types")
    body_fit_score: float = Field(..., ge=0.0, le=1.0, description="Body fit compatibility score")
    
    # Colors
    primary_colors: List[str] = Field(..., description="Primary colors in the outfit")
    color_palette: str = Field(..., description="Color palette description")
    
    # Social and trend data
    hashtags: List[str] = Field(default=[], description="Suggested hashtags")
    trend_score: float = Field(..., ge=0.0, le=1.0, description="Current trend score")
    social_media_score: Optional[float] = Field(None, description="Social media popularity score")
    
    # AI-generated content
    ai_caption: str = Field(..., description="AI-generated outfit caption")
    style_match_score: float = Field(..., ge=0.0, le=1.0, description="Style match score")
    
    # Metadata
    source: Optional[str] = Field(None, description="Data source")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")


class RecommendationRequest(BaseModel):
    """Request for outfit recommendations"""
    conversation_id: str = Field(..., description="Conversation ID")
    user_context: Dict[str, Any] = Field(..., description="User context from conversation")
    
    # Optional filters
    category: Optional[OutfitCategory] = Field(None, description="Filter by category")
    season: Optional[Season] = Field(None, description="Filter by season")
    max_price: Optional[float] = Field(None, description="Maximum price filter")
    min_price: Optional[float] = Field(None, description="Minimum price filter")
    body_type: Optional[BodyType] = Field(None, description="User's body type")
    color_preferences: List[str] = Field(default=[], description="Preferred colors")
    style_preferences: List[str] = Field(default=[], description="Preferred styles")
    
    # RAG parameters
    num_recommendations: int = Field(default=5, ge=1, le=20, description="Number of recommendations")
    similarity_threshold: float = Field(default=0.7, ge=0.0, le=1.0, description="Similarity threshold")
    include_alternatives: bool = Field(default=True, description="Include alternative options")


class RecommendationResponse(BaseModel):
    """Response with outfit recommendations"""
    recommendations: List[OutfitRecommendation] = Field(..., description="List of outfit recommendations")
    total_found: int = Field(..., description="Total number of matching outfits")
    query_context: Dict[str, Any] = Field(..., description="Context used for recommendations")
    processing_time: float = Field(..., description="Processing time in seconds")
    
    # RAG metadata
    vector_search_results: int = Field(..., description="Number of vector search results")
    filters_applied: List[str] = Field(default=[], description="Filters applied to search")
    
    # Personalization info
    personalization_score: float = Field(..., ge=0.0, le=1.0, description="Personalization effectiveness score")
    user_preference_match: float = Field(..., ge=0.0, le=1.0, description="User preference match score")


class SimilarOutfitsRequest(BaseModel):
    """Request for similar outfits"""
    outfit_id: str = Field(..., description="Reference outfit ID")
    num_similar: int = Field(default=5, ge=1, le=10, description="Number of similar outfits")
    similarity_threshold: float = Field(default=0.8, ge=0.0, le=1.0, description="Similarity threshold")
    
    # Optional filters
    same_category: bool = Field(default=True, description="Keep same category")
    same_price_range: bool = Field(default=False, description="Keep same price range")
    same_season: bool = Field(default=False, description="Keep same season")


class SimilarOutfitsResponse(BaseModel):
    """Response with similar outfits"""
    reference_outfit: OutfitRecommendation = Field(..., description="Reference outfit")
    similar_outfits: List[OutfitRecommendation] = Field(..., description="Similar outfits")
    similarity_scores: List[float] = Field(..., description="Similarity scores for each outfit")


class OutfitFeedbackRequest(BaseModel):
    """Request to provide feedback on outfit recommendation"""
    outfit_id: str = Field(..., description="Outfit ID")
    conversation_id: str = Field(..., description="Conversation ID")
    liked: bool = Field(..., description="Whether user liked the outfit")
    feedback_text: Optional[str] = Field(None, description="Optional feedback text")
    
    # Specific feedback categories
    style_rating: Optional[int] = Field(None, ge=1, le=5, description="Style rating (1-5)")
    fit_rating: Optional[int] = Field(None, ge=1, le=5, description="Fit rating (1-5)")
    price_rating: Optional[int] = Field(None, ge=1, le=5, description="Price rating (1-5)")
    overall_rating: Optional[int] = Field(None, ge=1, le=5, description="Overall rating (1-5)")


class OutfitFeedbackResponse(BaseModel):
    """Response after providing feedback"""
    success: bool = Field(..., description="Whether feedback was recorded")
    message: str = Field(..., description="Response message")
    updated_recommendations: bool = Field(..., description="Whether recommendations were updated")


class TrendingOutfitsRequest(BaseModel):
    """Request for trending outfits"""
    category: Optional[OutfitCategory] = Field(None, description="Filter by category")
    season: Optional[Season] = Field(None, description="Filter by season")
    time_period: str = Field(default="week", description="Time period: 'day', 'week', 'month'")
    limit: int = Field(default=10, ge=1, le=50, description="Number of trending outfits")


class TrendingOutfitsResponse(BaseModel):
    """Response with trending outfits"""
    trending_outfits: List[OutfitRecommendation] = Field(..., description="Trending outfits")
    trend_period: str = Field(..., description="Time period analyzed")
    trend_metrics: Dict[str, float] = Field(..., description="Trend analysis metrics")


class PersonalizedFeedRequest(BaseModel):
    """Request for personalized outfit feed"""
    user_id: str = Field(..., description="User ID")
    page: int = Field(default=1, ge=1, description="Page number")
    per_page: int = Field(default=20, ge=1, le=50, description="Items per page")
    
    # Personalization parameters
    include_new_trends: bool = Field(default=True, description="Include new trending items")
    include_similar_to_liked: bool = Field(default=True, description="Include items similar to liked ones")
    diversity_factor: float = Field(default=0.3, ge=0.0, le=1.0, description="Diversity vs relevance balance")


class PersonalizedFeedResponse(BaseModel):
    """Response with personalized outfit feed"""
    outfits: List[OutfitRecommendation] = Field(..., description="Personalized outfit feed")
    page: int = Field(..., description="Current page")
    per_page: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total pages available")
    personalization_factors: Dict[str, float] = Field(..., description="Personalization factors used")