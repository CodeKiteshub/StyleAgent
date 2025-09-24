"""
Pydantic schemas for image analysis API
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class AnalysisStatus(str, Enum):
    """Analysis status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class BodyType(str, Enum):
    """Body type enumeration"""
    PEAR = "pear"
    APPLE = "apple"
    HOURGLASS = "hourglass"
    RECTANGLE = "rectangle"
    INVERTED_TRIANGLE = "inverted_triangle"


class ClothingItem(BaseModel):
    """Clothing item detected in image"""
    category: str = Field(..., description="Clothing category (e.g., shirt, pants, dress)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detection confidence score")
    color: str = Field(..., description="Primary color of the item")
    style: Optional[str] = Field(None, description="Style description")
    bbox: Optional[List[float]] = Field(None, description="Bounding box coordinates [x1, y1, x2, y2]")


class PoseData(BaseModel):
    """Body pose analysis data"""
    keypoints: List[List[float]] = Field(..., description="Body keypoints coordinates")
    confidence_scores: List[float] = Field(..., description="Confidence scores for each keypoint")
    body_measurements: Optional[Dict[str, float]] = Field(None, description="Estimated body measurements")


class TrendElement(BaseModel):
    """Fashion trend element"""
    element: str = Field(..., description="Trend element name")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Trend confidence score")
    category: str = Field(..., description="Trend category")
    social_score: Optional[float] = Field(None, description="Social media popularity score")


class ImageAnalysisRequest(BaseModel):
    """Request schema for image analysis"""
    image_url: HttpUrl = Field(..., description="URL of the image to analyze")
    conversation_id: Optional[str] = Field(None, description="Associated conversation ID")
    analysis_type: str = Field(
        default="full", 
        description="Type of analysis: 'full', 'body_only', 'clothing_only', 'trend_only'"
    )
    include_recommendations: bool = Field(
        default=True, 
        description="Whether to include outfit recommendations"
    )


class ImageAnalysisResponse(BaseModel):
    """Response schema for image analysis"""
    analysis_id: str = Field(..., description="Unique analysis ID")
    status: AnalysisStatus = Field(..., description="Analysis status")
    image_url: HttpUrl = Field(..., description="Original image URL")
    
    # Image metadata
    image_width: Optional[int] = Field(None, description="Image width in pixels")
    image_height: Optional[int] = Field(None, description="Image height in pixels")
    
    # Body analysis
    body_type: Optional[BodyType] = Field(None, description="Predicted body type")
    body_type_confidence: Optional[float] = Field(None, description="Body type prediction confidence")
    pose_data: Optional[PoseData] = Field(None, description="Body pose analysis data")
    
    # Clothing detection
    clothing_items: List[ClothingItem] = Field(default=[], description="Detected clothing items")
    dominant_colors: List[str] = Field(default=[], description="Dominant colors in the outfit")
    style_attributes: List[str] = Field(default=[], description="Style attributes detected")
    
    # CLIP-ViT analysis
    clip_embeddings: Optional[List[float]] = Field(None, description="CLIP-ViT embeddings")
    style_description: Optional[str] = Field(None, description="AI-generated style description")
    
    # Trend analysis
    trend_elements: List[TrendElement] = Field(default=[], description="Fashion trend elements")
    overall_trend_score: Optional[float] = Field(None, description="Overall trend score")
    
    # Quality metrics
    image_quality_score: Optional[float] = Field(None, description="Image quality score")
    analysis_confidence: Optional[float] = Field(None, description="Overall analysis confidence")
    
    # Processing info
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Analysis creation time")
    
    # Error handling
    error_message: Optional[str] = Field(None, description="Error message if analysis failed")


class GetAnalysisResponse(BaseModel):
    """Response schema for getting analysis by ID"""
    analysis: ImageAnalysisResponse = Field(..., description="Image analysis data")


class ListAnalysesResponse(BaseModel):
    """Response schema for listing user's analyses"""
    analyses: List[ImageAnalysisResponse] = Field(..., description="List of image analyses")
    total: int = Field(..., description="Total number of analyses")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Items per page")


class AnalysisStatusResponse(BaseModel):
    """Response schema for analysis status check"""
    analysis_id: str = Field(..., description="Analysis ID")
    status: AnalysisStatus = Field(..., description="Current analysis status")
    progress: Optional[float] = Field(None, description="Analysis progress percentage")
    estimated_completion: Optional[datetime] = Field(None, description="Estimated completion time")
    error_message: Optional[str] = Field(None, description="Error message if failed")