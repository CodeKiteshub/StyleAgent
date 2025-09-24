"""
API routes for outfit recommendations
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import logging

from core.database import get_db
from schemas.recommendations import (
    RecommendationRequest, RecommendationResponse,
    SimilarOutfitsRequest, SimilarOutfitsResponse,
    OutfitFeedbackRequest, OutfitFeedbackResponse,
    TrendingOutfitsRequest, TrendingOutfitsResponse,
    PersonalizedFeedRequest, PersonalizedFeedResponse
)
from services.rag_service import RAGService
from services.trend_service import TrendService
from models.user import User
from models.outfit import OutfitRecommendation as OutfitRecommendationModel

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
rag_service = RAGService()
trend_service = TrendService()


@router.post("/generate", response_model=RecommendationResponse)
async def generate_recommendations(
    request: RecommendationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate outfit recommendations based on user context and preferences
    """
    try:
        # Get recommendations from RAG service
        recommendations, metadata = await rag_service.get_recommendations(request)
        
        # Note: User storage is skipped since RecommendationRequest doesn't include user_id
        # In a production system, you might get user_id from authentication context
        
        return RecommendationResponse(
            recommendations=recommendations,
            total_found=len(recommendations),
            query_context=request.user_context,
            processing_time=metadata.get("search_time", 0.1),
            vector_search_results=len(recommendations),
            filters_applied=list(metadata.get("filters_applied", {}).keys()),
            personalization_score=0.8,  # Mock score
            user_preference_match=0.75  # Mock score
        )
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations")


@router.post("", response_model=RecommendationResponse)
async def get_recommendations(
    request: RecommendationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Get outfit recommendations - matches frontend POST /recommendations call
    """
    try:
        # Get recommendations from RAG service
        recommendations, metadata = await rag_service.get_recommendations(request)
        
        # Note: User storage is skipped since RecommendationRequest doesn't include user_id
        # In a production system, you might get user_id from authentication context
        
        return RecommendationResponse(
            recommendations=recommendations,
            total_found=len(recommendations),
            query_context=request.user_context,
            processing_time=metadata.get("search_time", 0.1),
            vector_search_results=len(recommendations),
            filters_applied=list(metadata.get("filters_applied", {}).keys()),
            personalization_score=0.8,  # Mock score
            user_preference_match=0.75  # Mock score
        )
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations")


@router.get("/similar/{outfit_id}", response_model=SimilarOutfitsResponse)
async def get_similar_outfits(
    outfit_id: str,
    num_similar: int = Query(5, ge=1, le=20),
    similarity_threshold: float = Query(0.7, ge=0.0, le=1.0)
):
    """
    Get outfits similar to a specific outfit
    """
    try:
        similar_outfits = await rag_service.get_similar_outfits(
            outfit_id=outfit_id,
            num_similar=num_similar,
            similarity_threshold=similarity_threshold
        )
        
        return SimilarOutfitsResponse(
            reference_outfit_id=outfit_id,
            similar_outfits=similar_outfits,
            similarity_threshold=similarity_threshold
        )
        
    except Exception as e:
        logger.error(f"Error getting similar outfits: {e}")
        raise HTTPException(status_code=500, detail="Failed to get similar outfits")


@router.post("/feedback", response_model=OutfitFeedbackResponse)
async def submit_outfit_feedback(
    request: OutfitFeedbackRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Submit feedback for an outfit recommendation
    """
    try:
        # Update recommendation in database
        if request.user_id:
            # Find the recommendation record
            from sqlalchemy import select
            
            stmt = select(OutfitRecommendationModel).where(
                OutfitRecommendationModel.user_id == request.user_id,
                OutfitRecommendationModel.outfit_id == request.outfit_id
            )
            result = await db.execute(stmt)
            recommendation = result.scalar_one_or_none()
            
            if recommendation:
                # Update feedback fields
                recommendation.user_liked = request.liked
                recommendation.user_saved = request.saved
                recommendation.user_purchased = request.purchased
                
                await db.commit()
        
        # Process feedback for learning (simplified)
        feedback_processed = True
        
        return OutfitFeedbackResponse(
            success=feedback_processed,
            message="Feedback received successfully"
        )
        
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit feedback")


@router.get("/trending", response_model=TrendingOutfitsResponse)
async def get_trending_outfits(
    category: Optional[str] = Query(None),
    season: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=50)
):
    """
    Get currently trending outfits
    """
    try:
        trending_outfits = await trend_service.get_trending_outfits(
            category=category,
            season=season,
            limit=limit
        )
        
        return TrendingOutfitsResponse(
            trending_outfits=trending_outfits,
            trend_period="current_week",
            last_updated=trend_service.get_last_update_time()
        )
        
    except Exception as e:
        logger.error(f"Error getting trending outfits: {e}")
        raise HTTPException(status_code=500, detail="Failed to get trending outfits")


@router.post("/personalized-feed", response_model=PersonalizedFeedResponse)
async def get_personalized_feed(
    request: PersonalizedFeedRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Get personalized outfit feed based on user preferences and history
    """
    try:
        # Get user preferences
        user = await db.get(User, request.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Create recommendation request based on user profile
        rec_request = RecommendationRequest(
            user_id=request.user_id,
            user_context={
                'style_preference': user.style_preference,
                'color_preferences': user.preferred_colors,
                'budget': user.budget_range,
                'occasion': 'casual'  # Default for feed
            },
            num_recommendations=request.limit,
            category=None,
            season=None,
            body_type=user.body_type
        )
        
        # Get recommendations
        recommendations, metadata = await rag_service.get_recommendations(rec_request)
        
        # Mix with trending items
        trending_outfits = await trend_service.get_trending_outfits(limit=5)
        
        # Combine and shuffle (simplified algorithm)
        feed_items = recommendations[:request.limit - len(trending_outfits)] + trending_outfits
        
        return PersonalizedFeedResponse(
            feed_items=feed_items,
            user_id=request.user_id,
            personalization_score=0.85,  # Mock score
            refresh_token=f"refresh_{request.user_id}_{len(feed_items)}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting personalized feed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get personalized feed")


@router.get("/user/{user_id}/history")
async def get_user_recommendation_history(
    user_id: str,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user's recommendation history
    """
    try:
        from sqlalchemy import select, desc
        
        stmt = select(OutfitRecommendationModel).where(
            OutfitRecommendationModel.user_id == user_id
        ).order_by(
            desc(OutfitRecommendationModel.created_at)
        ).offset(offset).limit(limit)
        
        result = await db.execute(stmt)
        recommendations = result.scalars().all()
        
        return {
            "recommendations": [
                {
                    "outfit_id": rec.outfit_id,
                    "relevance_score": rec.relevance_score,
                    "ai_caption": rec.ai_caption,
                    "user_liked": rec.user_liked,
                    "user_saved": rec.user_saved,
                    "created_at": rec.created_at
                }
                for rec in recommendations
            ],
            "total_count": len(recommendations),
            "offset": offset,
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"Error getting recommendation history: {e}")
        raise HTTPException(status_code=500, detail="Failed to get recommendation history")


@router.post("/refresh-index")
async def refresh_recommendation_index(
    background_tasks: BackgroundTasks
):
    """
    Refresh the recommendation index (admin endpoint)
    """
    try:
        # Add background task to refresh index
        background_tasks.add_task(refresh_index_task)
        
        return {"message": "Index refresh started"}
        
    except Exception as e:
        logger.error(f"Error starting index refresh: {e}")
        raise HTTPException(status_code=500, detail="Failed to start index refresh")


async def refresh_index_task():
    """Background task to refresh the recommendation index"""
    try:
        logger.info("Starting recommendation index refresh")
        
        # In a real implementation, you would:
        # 1. Fetch all outfits from database
        # 2. Generate embeddings for each
        # 3. Update Pinecone index
        # 4. Update trend scores
        
        # For now, we'll just log
        logger.info("Index refresh completed")
        
    except Exception as e:
        logger.error(f"Error in index refresh task: {e}")


@router.get("/stats")
async def get_recommendation_stats(
    db: AsyncSession = Depends(get_db)
):
    """
    Get recommendation system statistics
    """
    try:
        from sqlalchemy import select, func
        
        # Get total recommendations count
        total_stmt = select(func.count(OutfitRecommendationModel.id))
        total_result = await db.execute(total_stmt)
        total_recommendations = total_result.scalar()
        
        # Get liked recommendations count
        liked_stmt = select(func.count(OutfitRecommendationModel.id)).where(
            OutfitRecommendationModel.user_liked == True
        )
        liked_result = await db.execute(liked_stmt)
        liked_recommendations = liked_result.scalar()
        
        # Calculate engagement rate
        engagement_rate = (liked_recommendations / total_recommendations * 100) if total_recommendations > 0 else 0
        
        return {
            "total_recommendations": total_recommendations,
            "liked_recommendations": liked_recommendations,
            "engagement_rate": round(engagement_rate, 2),
            "index_status": "healthy",  # Mock status
            "last_updated": "2024-01-15T10:00:00Z"  # Mock timestamp
        }
        
    except Exception as e:
        logger.error(f"Error getting recommendation stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get recommendation stats")