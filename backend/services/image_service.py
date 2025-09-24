"""
Simplified image analysis service for testing
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
import asyncio
from dataclasses import dataclass

from core.config import settings

logger = logging.getLogger(__name__)


@dataclass
class AnalysisResult:
    """Result of image analysis"""
    body_type: Optional[str] = None
    body_type_confidence: Optional[float] = None
    pose_data: Optional[Dict] = None
    clothing_items: List[Dict] = None
    dominant_colors: List[str] = None
    style_attributes: List[str] = None
    clip_embeddings: Optional[List[float]] = None
    style_description: Optional[str] = None
    trend_elements: List[Dict] = None
    overall_trend_score: Optional[float] = None
    image_quality_score: Optional[float] = None
    analysis_confidence: Optional[float] = None
    processing_time: Optional[float] = None


class ImageAnalysisService:
    """Simplified image analysis service for testing purposes"""
    
    def __init__(self):
        """Initialize the service"""
        self.logger = logging.getLogger(__name__)
        self.logger.info("ImageAnalysisService initialized (simplified version)")
    
    async def download_image(self, image_url: str) -> Optional[Any]:
        """Mock image download"""
        self.logger.info(f"Mock downloading image from: {image_url}")
        return {"mock_image": True, "url": image_url}
    
    def analyze_body_pose(self, image: Any) -> Optional[Dict]:
        """Mock body pose analysis"""
        return {
            "keypoints": [],
            "confidence": 0.8,
            "mock": True
        }
    
    def predict_body_type(self, pose_data: Dict) -> Tuple[Optional[str], Optional[float]]:
        """Mock body type prediction"""
        return "rectangle", 0.75
    
    def detect_colors(self, image: Any) -> List[str]:
        """Mock color detection"""
        return ["#FF5733", "#33FF57", "#3357FF"]
    
    async def analyze_with_clip(self, image: Any) -> Tuple[Optional[List[float]], Optional[str], List[str]]:
        """Mock CLIP analysis"""
        embeddings = [0.1] * 512  # Mock 512-dimensional embedding
        description = "A stylish outfit with modern elements"
        attributes = ["casual", "modern", "comfortable"]
        return embeddings, description, attributes
    
    def detect_clothing_items(self, image: Any) -> List[Dict]:
        """Mock clothing detection"""
        return [
            {
                "type": "shirt",
                "confidence": 0.9,
                "color": "#FF5733",
                "style": "casual"
            },
            {
                "type": "pants",
                "confidence": 0.85,
                "color": "#3357FF",
                "style": "jeans"
            }
        ]
    
    def analyze_trends(self, style_attributes: List[str], clothing_items: List[Dict]) -> Tuple[List[Dict], Optional[float]]:
        """Mock trend analysis"""
        trends = [
            {
                "name": "Casual Chic",
                "confidence": 0.8,
                "description": "Relaxed yet stylish"
            }
        ]
        return trends, 0.75
    
    def calculate_image_quality(self, image: Any) -> float:
        """Mock image quality calculation"""
        return 0.85
    
    async def analyze_image(self, image_url: str, analysis_type: str = "full") -> AnalysisResult:
        """Mock comprehensive image analysis"""
        self.logger.info(f"Mock analyzing image: {image_url} (type: {analysis_type})")
        
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        # Mock analysis results
        result = AnalysisResult(
            body_type="rectangle",
            body_type_confidence=0.75,
            pose_data={"mock": True},
            clothing_items=[
                {"type": "shirt", "confidence": 0.9},
                {"type": "pants", "confidence": 0.85}
            ],
            dominant_colors=["#FF5733", "#33FF57", "#3357FF"],
            style_attributes=["casual", "modern", "comfortable"],
            clip_embeddings=[0.1] * 512,
            style_description="A stylish outfit with modern elements",
            trend_elements=[
                {"name": "Casual Chic", "confidence": 0.8}
            ],
            overall_trend_score=0.75,
            image_quality_score=0.85,
            analysis_confidence=0.8,
            processing_time=0.1
        )
        
        return result