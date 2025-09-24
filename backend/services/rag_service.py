"""
Simplified RAG service for testing
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
import asyncio
from dataclasses import dataclass

from core.config import settings

logger = logging.getLogger(__name__)


@dataclass
class VectorSearchResult:
    """Vector search result data class"""
    outfit_id: str
    score: float
    metadata: Dict[str, Any]


class RAGService:
    """Simplified RAG service for testing purposes"""
    
    def __init__(self):
        """Initialize the service"""
        self.logger = logging.getLogger(__name__)
        self.logger.info("RAGService initialized (simplified version)")
        
        # Mock outfit database
        self.mock_outfits = [
            {
                "id": "outfit_1",
                "category": "casual",
                "season": "spring",
                "body_type": "rectangle",
                "items": [
                    {"type": "shirt", "color": "blue", "brand": "Brand A"},
                    {"type": "jeans", "color": "dark_blue", "brand": "Brand B"}
                ],
                "style_tags": ["casual", "comfortable", "everyday"],
                "price_range": "medium"
            },
            {
                "id": "outfit_2",
                "category": "formal",
                "season": "all_season",
                "body_type": "hourglass",
                "items": [
                    {"type": "blazer", "color": "black", "brand": "Brand C"},
                    {"type": "dress_pants", "color": "black", "brand": "Brand D"}
                ],
                "style_tags": ["formal", "professional", "elegant"],
                "price_range": "high"
            },
            {
                "id": "outfit_3",
                "category": "casual",
                "season": "summer",
                "body_type": "pear",
                "items": [
                    {"type": "t_shirt", "color": "white", "brand": "Brand E"},
                    {"type": "shorts", "color": "khaki", "brand": "Brand F"}
                ],
                "style_tags": ["casual", "trendy", "urban"],
                "price_range": "low"
            }
        ]
    
    def create_query_embedding(self, user_context: Dict[str, Any]) -> List[float]:
        """Mock query embedding creation"""
        # Return a mock embedding vector
        return [0.1] * 384
    
    def apply_filters(self, request: Any) -> Dict[str, Any]:
        """Mock filter application"""
        return {
            "category": getattr(request, 'category', None),
            "season": getattr(request, 'season', None),
            "body_type": getattr(request, 'body_type', None),
            "price_range": getattr(request, 'price_range', None)
        }
    
    async def vector_search(
        self, 
        query_embedding: List[float], 
        filters: Dict[str, Any],
        top_k: int = 50
    ) -> List[VectorSearchResult]:
        """Mock vector search"""
        results = []
        
        for outfit in self.mock_outfits:
            # Simple filtering logic
            matches = True
            
            if filters.get('category') and outfit['category'] != filters['category']:
                matches = False
            if filters.get('season') and outfit['season'] not in ['all', filters['season']]:
                matches = False
            if filters.get('body_type') and outfit['body_type'] != filters['body_type']:
                matches = False
            if filters.get('price_range') and outfit['price_range'] != filters['price_range']:
                matches = False
            
            if matches:
                results.append(VectorSearchResult(
                    outfit_id=outfit['id'],
                    score=0.85,  # Mock similarity score
                    metadata=outfit
                ))
        
        return results[:top_k]
    
    def rerank_results(
        self, 
        results: List[VectorSearchResult], 
        user_context: Dict[str, Any]
    ) -> List[VectorSearchResult]:
        """Mock result reranking"""
        # Simple reranking based on score
        return sorted(results, key=lambda x: x.score, reverse=True)
    
    def convert_to_recommendations(
        self, 
        results: List[VectorSearchResult]
    ) -> List[Dict[str, Any]]:
        """Convert search results to recommendations"""
        recommendations = []
        
        for result in results:
            metadata = result.metadata
            recommendations.append({
                "outfit_id": result.outfit_id,
                "title": f"{metadata.get('category', 'Stylish').title()} Outfit",
                "description": f"A perfect {metadata.get('category', 'casual')} outfit for your style",
                "image_url": "https://example.com/outfit-image.jpg",
                
                # Style attributes
                "category": metadata.get('category', 'casual'),
                "occasion": metadata.get('occasion', 'everyday'),
                "season": metadata.get('season', 'all_season'),
                "style_tags": metadata.get('style_tags', ['comfortable', 'stylish']),
                
                # Clothing items - ensure each item has required fields
                "items": [
                    {
                        "category": item.get('type', 'clothing'),
                        "brand": item.get('brand', 'Unknown'),
                        "color": item.get('color', 'neutral'),
                        "size_range": ["S", "M", "L", "XL"],
                        "price": item.get('price', 50.0),
                        "url": None
                    } for item in metadata.get('items', [])
                ],
                
                # Pricing
                "total_price": metadata.get('total_price', 150.0),
                "price_range": metadata.get('price_range', 'medium'),
                
                # Body compatibility
                "body_types": [metadata.get('body_type', 'rectangle')],
                "body_fit_score": 0.85,
                
                # Colors
                "primary_colors": metadata.get('primary_colors', ['neutral', 'blue']),
                "color_palette": metadata.get('color_palette', 'neutral tones'),
                
                # Social and trend data
                "hashtags": ["#style", "#fashion", "#outfit"],
                "trend_score": 0.75,
                "social_media_score": 0.8,
                
                # AI-generated content
                "ai_caption": f"A {metadata.get('category', 'stylish')} outfit perfect for your style",
                "style_match_score": result.score,
                
                # Metadata
                "source": "mock_data",
                "created_at": "2024-01-01T00:00:00Z"
            })
        
        return recommendations
    
    async def generate_ai_captions(
        self, 
        recommendations: List[Dict[str, Any]],
        user_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Mock AI caption generation"""
        for rec in recommendations:
            category = rec.get('category', 'stylish')
            rec['ai_caption'] = f"A {category} outfit that matches your personal style perfectly"
        
        return recommendations
    
    async def get_recommendations(
        self, 
        request: Any
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Mock recommendation generation"""
        self.logger.info("Generating mock recommendations")
        
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        # Create mock user context
        user_context = {
            "body_type": getattr(request, 'body_type', 'rectangle'),
            "style_preferences": getattr(request, 'style_preferences', ['casual']),
            "season": getattr(request, 'season', 'spring'),
            "occasion": getattr(request, 'occasion', 'everyday')
        }
        
        # Create query embedding
        query_embedding = self.create_query_embedding(user_context)
        
        # Apply filters
        filters = self.apply_filters(request)
        
        # Perform vector search
        search_results = await self.vector_search(query_embedding, filters)
        
        # Rerank results
        reranked_results = self.rerank_results(search_results, user_context)
        
        # Convert to recommendations
        recommendations = self.convert_to_recommendations(reranked_results)
        
        # Generate AI captions
        recommendations = await self.generate_ai_captions(recommendations, user_context)
        
        # Metadata about the search
        metadata = {
            "total_results": len(recommendations),
            "search_time": 0.1,
            "filters_applied": filters,
            "query_type": "mock_search"
        }
        
        return recommendations, metadata
    
    async def get_similar_outfits(
        self, 
        outfit_id: str, 
        num_similar: int = 5,
        similarity_threshold: float = 0.8
    ) -> List[Dict[str, Any]]:
        """Mock similar outfit search"""
        self.logger.info(f"Finding similar outfits to {outfit_id}")
        
        # Find the base outfit
        base_outfit = None
        for outfit in self.mock_outfits:
            if outfit['id'] == outfit_id:
                base_outfit = outfit
                break
        
        if not base_outfit:
            return []
        
        # Find similar outfits (mock logic)
        similar_outfits = []
        for outfit in self.mock_outfits:
            if outfit['id'] != outfit_id:
                # Simple similarity based on category
                if outfit['category'] == base_outfit['category']:
                    similar_outfits.append({
                        "id": outfit['id'],
                        "category": outfit['category'],
                        "season": outfit['season'],
                        "body_type": outfit['body_type'],
                        "items": outfit['items'],
                        "style_tags": outfit['style_tags'],
                        "price_range": outfit['price_range'],
                        "similarity_score": 0.85,
                        "ai_caption": f"Similar {outfit['category']} style to your selected outfit"
                    })
        
        return similar_outfits[:num_similar]
    
    async def add_outfit_to_index(self, outfit_data: Dict[str, Any]) -> bool:
        """Mock outfit indexing"""
        self.logger.info(f"Mock adding outfit to index: {outfit_data.get('id', 'unknown')}")
        return True