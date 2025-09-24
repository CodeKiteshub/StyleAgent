"""
Simplified social media trend analysis service for testing
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import re
from collections import Counter

from core.config import settings

logger = logging.getLogger(__name__)


@dataclass
class TrendData:
    """Trend data structure"""
    keyword: str
    mentions: int
    growth_rate: float
    sentiment_score: float
    hashtags: List[str]
    platforms: Dict[str, int]


@dataclass
class SocialMediaPost:
    """Social media post data"""
    platform: str
    content: str
    hashtags: List[str]
    likes: int
    shares: int
    comments: int
    timestamp: datetime


class TrendService:
    """Simplified service for analyzing social media trends and fashion popularity"""
    
    def __init__(self):
        self.trend_keywords = {
            'fashion': [
                'outfit', 'style', 'fashion', 'ootd', 'look', 'wear', 'clothing',
                'dress', 'shirt', 'pants', 'shoes', 'accessories', 'jewelry'
            ],
            'seasonal': [
                'spring', 'summer', 'fall', 'winter', 'autumn',
                'warm', 'cold', 'hot', 'cool', 'weather'
            ],
            'occasions': [
                'work', 'casual', 'formal', 'party', 'date', 'wedding',
                'business', 'weekend', 'vacation', 'travel'
            ],
            'styles': [
                'minimalist', 'boho', 'streetwear', 'classic', 'trendy',
                'vintage', 'modern', 'chic', 'elegant', 'edgy'
            ]
        }
        
        # Mock trending data
        self.mock_trends = [
            TrendData(
                keyword="oversized blazers",
                mentions=15420,
                growth_rate=0.35,
                sentiment_score=0.82,
                hashtags=["#oversizedblazer", "#workwear", "#professional"],
                platforms={"instagram": 8500, "tiktok": 4200, "pinterest": 2720}
            ),
            TrendData(
                keyword="cottagecore aesthetic",
                mentions=12800,
                growth_rate=0.28,
                sentiment_score=0.89,
                hashtags=["#cottagecore", "#vintage", "#romantic"],
                platforms={"instagram": 7200, "tiktok": 3600, "pinterest": 2000}
            ),
            TrendData(
                keyword="sustainable fashion",
                mentions=18900,
                growth_rate=0.42,
                sentiment_score=0.91,
                hashtags=["#sustainablefashion", "#ecofriendly", "#ethical"],
                platforms={"instagram": 10500, "tiktok": 5400, "pinterest": 3000}
            )
        ]
    
    def _generate_mock_social_data(self) -> List[SocialMediaPost]:
        """Generate mock social media data"""
        mock_posts = [
            {
                "platform": "instagram",
                "content": "Loving this oversized blazer look for work! #ootd #workwear #professional",
                "hashtags": ["ootd", "workwear", "professional", "oversizedblazer"],
                "likes": 1250,
                "shares": 45,
                "comments": 89,
                "timestamp": datetime.now() - timedelta(hours=2)
            },
            {
                "platform": "tiktok",
                "content": "Cottagecore vibes with this flowy dress and vintage accessories",
                "hashtags": ["cottagecore", "vintage", "romantic", "dress"],
                "likes": 8900,
                "shares": 234,
                "comments": 156,
                "timestamp": datetime.now() - timedelta(hours=5)
            },
            {
                "platform": "pinterest",
                "content": "Sustainable fashion haul - thrifted finds and eco-friendly brands",
                "hashtags": ["sustainablefashion", "thrifted", "ecofriendly"],
                "likes": 567,
                "shares": 123,
                "comments": 34,
                "timestamp": datetime.now() - timedelta(hours=8)
            },
            {
                "platform": "instagram",
                "content": "Streetwear meets minimalism in this clean look",
                "hashtags": ["streetwear", "minimalist", "clean", "urban"],
                "likes": 2100,
                "shares": 78,
                "comments": 92,
                "timestamp": datetime.now() - timedelta(hours=12)
            }
        ]
        
        return [SocialMediaPost(**post) for post in mock_posts]
    
    async def analyze_hashtag_trends(self, hashtags: List[str]) -> Dict[str, float]:
        """Mock hashtag trend analysis"""
        logger.info(f"Analyzing hashtag trends for: {hashtags}")
        
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        trend_scores = {}
        for hashtag in hashtags:
            # Mock trend score calculation
            base_score = 0.5
            
            # Boost score for popular hashtags
            if any(keyword in hashtag.lower() for keyword in ['ootd', 'fashion', 'style']):
                base_score += 0.3
            if any(keyword in hashtag.lower() for keyword in ['sustainable', 'eco', 'ethical']):
                base_score += 0.25
            if any(keyword in hashtag.lower() for keyword in ['vintage', 'retro', 'classic']):
                base_score += 0.2
            
            trend_scores[hashtag] = min(base_score, 1.0)
        
        return trend_scores
    
    async def get_trending_keywords(self, category: Optional[str] = None) -> List[TrendData]:
        """Mock trending keywords retrieval"""
        logger.info(f"Getting trending keywords for category: {category}")
        
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        if category:
            # Filter trends by category
            filtered_trends = []
            for trend in self.mock_trends:
                if category.lower() in trend.keyword.lower():
                    filtered_trends.append(trend)
            return filtered_trends
        
        return self.mock_trends
    
    async def calculate_outfit_trend_score(self, outfit_data: Dict[str, Any]) -> float:
        """Mock outfit trend score calculation"""
        logger.info(f"Calculating trend score for outfit: {outfit_data.get('id', 'unknown')}")
        
        # Simulate processing time
        await asyncio.sleep(0.05)
        
        base_score = 0.5
        
        # Analyze outfit attributes
        style_tags = outfit_data.get('style_tags', [])
        category = outfit_data.get('category', '')
        items = outfit_data.get('items', [])
        
        # Boost score based on trending elements
        for tag in style_tags:
            if 'sustainable' in tag.lower():
                base_score += 0.2
            elif 'vintage' in tag.lower() or 'retro' in tag.lower():
                base_score += 0.15
            elif 'minimalist' in tag.lower():
                base_score += 0.1
            elif 'streetwear' in tag.lower():
                base_score += 0.12
        
        # Category-based scoring
        if 'formal' in category.lower() or 'work' in category.lower():
            base_score += 0.1
        elif 'casual' in category.lower():
            base_score += 0.05
        
        # Item-based scoring
        for item in items:
            item_type = item.get('type', '').lower()
            if 'blazer' in item_type:
                base_score += 0.08
            elif 'dress' in item_type:
                base_score += 0.06
            elif 'jeans' in item_type:
                base_score += 0.04
        
        return min(base_score, 1.0)
    
    async def get_trending_outfits(
        self, 
        category: Optional[str] = None,
        season: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Mock trending outfits retrieval"""
        logger.info(f"Getting trending outfits - category: {category}, season: {season}")
        
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        mock_outfits = [
            {
                "id": "trending_outfit_1",
                "title": "Oversized Blazer Power Look",
                "description": "Professional yet comfortable oversized blazer with tailored pants",
                "category": "formal",
                "season": "all",
                "style_tags": ["professional", "modern", "comfortable"],
                "items": [
                    {"type": "blazer", "color": "navy", "brand": "Professional Brand"},
                    {"type": "pants", "color": "black", "brand": "Work Wear Co"}
                ],
                "trend_score": 0.89,
                "social_mentions": 15420,
                "hashtags": ["#oversizedblazer", "#workwear", "#professional"]
            },
            {
                "id": "trending_outfit_2",
                "title": "Cottagecore Romance",
                "description": "Flowing dress with vintage accessories for a romantic look",
                "category": "casual",
                "season": "spring",
                "style_tags": ["romantic", "vintage", "feminine"],
                "items": [
                    {"type": "dress", "color": "floral", "brand": "Vintage Style"},
                    {"type": "cardigan", "color": "cream", "brand": "Cozy Knits"}
                ],
                "trend_score": 0.85,
                "social_mentions": 12800,
                "hashtags": ["#cottagecore", "#vintage", "#romantic"]
            },
            {
                "id": "trending_outfit_3",
                "title": "Sustainable Chic",
                "description": "Eco-friendly pieces that don't compromise on style",
                "category": "casual",
                "season": "summer",
                "style_tags": ["sustainable", "eco-friendly", "modern"],
                "items": [
                    {"type": "top", "color": "white", "brand": "Eco Fashion"},
                    {"type": "jeans", "color": "blue", "brand": "Sustainable Denim"}
                ],
                "trend_score": 0.92,
                "social_mentions": 18900,
                "hashtags": ["#sustainablefashion", "#ecofriendly", "#ethical"]
            }
        ]
        
        # Apply filters
        filtered_outfits = mock_outfits
        
        if category:
            filtered_outfits = [
                outfit for outfit in filtered_outfits 
                if outfit['category'].lower() == category.lower()
            ]
        
        if season:
            filtered_outfits = [
                outfit for outfit in filtered_outfits 
                if outfit['season'].lower() in [season.lower(), 'all']
            ]
        
        return filtered_outfits[:limit]
    
    async def update_trend_database(self) -> bool:
        """Mock trend database update"""
        logger.info("Mock updating trend database")
        await asyncio.sleep(0.1)
        return True
    
    def get_last_update_time(self) -> datetime:
        """Mock last update time"""
        return datetime.now() - timedelta(hours=1)
    
    async def analyze_social_media_post(self, post_content: str, hashtags: List[str]) -> Dict[str, Any]:
        """Mock social media post analysis"""
        logger.info(f"Analyzing social media post with {len(hashtags)} hashtags")
        
        # Simulate processing time
        await asyncio.sleep(0.05)
        
        # Mock sentiment analysis
        sentiment_score = 0.7  # Default positive sentiment
        
        # Simple keyword-based sentiment adjustment
        positive_words = ['love', 'amazing', 'perfect', 'beautiful', 'stunning']
        negative_words = ['hate', 'ugly', 'terrible', 'awful', 'disappointing']
        
        content_lower = post_content.lower()
        for word in positive_words:
            if word in content_lower:
                sentiment_score += 0.1
        for word in negative_words:
            if word in content_lower:
                sentiment_score -= 0.2
        
        sentiment_score = max(0.0, min(1.0, sentiment_score))
        
        # Extract fashion-related keywords
        fashion_keywords = []
        for category, keywords in self.trend_keywords.items():
            for keyword in keywords:
                if keyword.lower() in content_lower:
                    fashion_keywords.append(keyword)
        
        return {
            "sentiment_score": sentiment_score,
            "fashion_keywords": fashion_keywords,
            "hashtag_relevance": {hashtag: 0.8 for hashtag in hashtags},
            "trend_potential": min(sentiment_score + len(fashion_keywords) * 0.1, 1.0),
            "engagement_prediction": {
                "likes": int(sentiment_score * 1000),
                "shares": int(sentiment_score * 100),
                "comments": int(sentiment_score * 50)
            }
        }