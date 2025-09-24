"""
Image analysis API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid
from datetime import datetime
import logging

from core.database import get_db
from models.image_analysis import ImageAnalysis
from models.user import User
from schemas.image import (
    ImageAnalysisRequest, ImageAnalysisResponse, GetAnalysisResponse,
    ListAnalysesResponse, AnalysisStatusResponse, AnalysisStatus
)
from services.image_service import ImageAnalysisService

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize image analysis service
image_service = ImageAnalysisService()


@router.post("/upload-url", response_model=dict)
async def upload_image_from_url(
    request: dict,
    db: AsyncSession = Depends(get_db)
):
    """Upload image from URL for analysis"""
    try:
        image_url = request.get("image_url")
        if not image_url:
            raise HTTPException(status_code=400, detail="image_url is required")
        
        # Create a simple response that matches frontend expectations
        import uuid
        from datetime import datetime
        
        response = {
            "id": str(uuid.uuid4()),
            "url": image_url,
            "filename": image_url.split("/")[-1] if "/" in image_url else "uploaded_image",
            "size": 0,  # We don't know the actual size from URL
            "content_type": "image/jpeg",  # Default assumption
            "created_at": datetime.utcnow().isoformat()
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Error uploading image from URL: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload image from URL")


async def process_image_analysis(
    analysis_id: str,
    image_url: str,
    analysis_type: str,
    db: AsyncSession
):
    """Background task to process image analysis"""
    try:
        # Update status to processing
        stmt = select(ImageAnalysis).where(ImageAnalysis.id == analysis_id)
        result = await db.execute(stmt)
        analysis = result.scalar_one_or_none()
        
        if analysis:
            analysis.status = "processing"
            analysis.processing_started_at = datetime.utcnow()
            await db.commit()
        
        # Perform analysis
        result = await image_service.analyze_image(image_url, analysis_type)
        
        # Update database with results
        if analysis:
            analysis.status = "completed"
            analysis.processing_completed_at = datetime.utcnow()
            analysis.processing_time = result.processing_time
            
            # Body analysis
            if result.body_type:
                analysis.body_type_prediction = result.body_type.value
                analysis.body_type_confidence = result.body_type_confidence
            
            if result.pose_data:
                analysis.pose_keypoints = result.pose_data.keypoints
                analysis.pose_confidence_scores = result.pose_data.confidence_scores
                analysis.body_measurements = result.pose_data.body_measurements
            
            # Clothing detection
            if result.clothing_items:
                analysis.detected_clothing = [
                    {
                        "category": item.category,
                        "confidence": item.confidence,
                        "color": item.color,
                        "style": item.style,
                        "bbox": item.bbox
                    }
                    for item in result.clothing_items
                ]
            
            analysis.dominant_colors = result.dominant_colors
            analysis.style_attributes = result.style_attributes
            
            # CLIP analysis
            if result.clip_embeddings:
                analysis.clip_embeddings = result.clip_embeddings
            analysis.style_description = result.style_description
            
            # Trend analysis
            if result.trend_elements:
                analysis.trend_elements = [
                    {
                        "element": elem.element,
                        "confidence": elem.confidence,
                        "category": elem.category,
                        "social_score": elem.social_score
                    }
                    for elem in result.trend_elements
                ]
            
            analysis.overall_trend_score = result.overall_trend_score
            
            # Quality metrics
            analysis.image_quality_score = result.image_quality_score
            analysis.analysis_confidence = result.analysis_confidence
            
            await db.commit()
            
    except Exception as e:
        logger.error(f"Error processing image analysis {analysis_id}: {e}")
        
        # Update status to failed
        if analysis:
            analysis.status = "failed"
            analysis.error_message = str(e)
            analysis.processing_completed_at = datetime.utcnow()
            await db.commit()


@router.post("/analyze", response_model=ImageAnalysisResponse)
async def analyze_image(
    request: ImageAnalysisRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Start image analysis process
    """
    try:
        # Create analysis record
        analysis_id = str(uuid.uuid4())
        
        analysis = ImageAnalysis(
            id=analysis_id,
            image_url=str(request.image_url),
            conversation_id=request.conversation_id,
            analysis_type=request.analysis_type,
            status="pending",
            created_at=datetime.utcnow()
        )
        
        db.add(analysis)
        await db.commit()
        
        # Start background processing
        background_tasks.add_task(
            process_image_analysis,
            analysis_id,
            str(request.image_url),
            request.analysis_type,
            db
        )
        
        # Return initial response
        return ImageAnalysisResponse(
            analysis_id=analysis_id,
            status=AnalysisStatus.PENDING,
            image_url=request.image_url,
            created_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error starting image analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to start image analysis")


@router.get("/analysis/{analysis_id}", response_model=GetAnalysisResponse)
async def get_analysis(
    analysis_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get image analysis results by ID
    """
    try:
        stmt = select(ImageAnalysis).where(ImageAnalysis.id == analysis_id)
        result = await db.execute(stmt)
        analysis = result.scalar_one_or_none()
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        # Convert to response model
        response = ImageAnalysisResponse(
            analysis_id=analysis.id,
            status=AnalysisStatus(analysis.status),
            image_url=analysis.image_url,
            image_width=analysis.image_width,
            image_height=analysis.image_height,
            created_at=analysis.created_at,
            processing_time=analysis.processing_time
        )
        
        # Add body analysis data
        if analysis.body_type_prediction:
            from schemas.image import BodyType
            response.body_type = BodyType(analysis.body_type_prediction)
            response.body_type_confidence = analysis.body_type_confidence
        
        if analysis.pose_keypoints:
            from schemas.image import PoseData
            response.pose_data = PoseData(
                keypoints=analysis.pose_keypoints,
                confidence_scores=analysis.pose_confidence_scores or [],
                body_measurements=analysis.body_measurements
            )
        
        # Add clothing detection data
        if analysis.detected_clothing:
            from schemas.image import ClothingItem
            response.clothing_items = [
                ClothingItem(**item) for item in analysis.detected_clothing
            ]
        
        response.dominant_colors = analysis.dominant_colors or []
        response.style_attributes = analysis.style_attributes or []
        
        # Add CLIP analysis data
        response.clip_embeddings = analysis.clip_embeddings
        response.style_description = analysis.style_description
        
        # Add trend analysis data
        if analysis.trend_elements:
            from schemas.image import TrendElement
            response.trend_elements = [
                TrendElement(**elem) for elem in analysis.trend_elements
            ]
        
        response.overall_trend_score = analysis.overall_trend_score
        
        # Add quality metrics
        response.image_quality_score = analysis.image_quality_score
        response.analysis_confidence = analysis.analysis_confidence
        
        # Add error message if failed
        if analysis.status == "failed":
            response.error_message = analysis.error_message
        
        return GetAnalysisResponse(analysis=response)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting analysis {analysis_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get analysis")


@router.get("/analysis/{analysis_id}/status", response_model=AnalysisStatusResponse)
async def get_analysis_status(
    analysis_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get analysis status
    """
    try:
        stmt = select(ImageAnalysis).where(ImageAnalysis.id == analysis_id)
        result = await db.execute(stmt)
        analysis = result.scalar_one_or_none()
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        # Calculate progress
        progress = None
        if analysis.status == "processing":
            # Simple progress estimation based on time elapsed
            if analysis.processing_started_at:
                elapsed = (datetime.utcnow() - analysis.processing_started_at).total_seconds()
                # Assume average processing time is 30 seconds
                progress = min(elapsed / 30.0 * 100, 95)  # Cap at 95% until complete
        elif analysis.status == "completed":
            progress = 100.0
        elif analysis.status == "failed":
            progress = 0.0
        
        return AnalysisStatusResponse(
            analysis_id=analysis_id,
            status=AnalysisStatus(analysis.status),
            progress=progress,
            error_message=analysis.error_message
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting analysis status {analysis_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get analysis status")


@router.get("/analyses", response_model=ListAnalysesResponse)
async def list_user_analyses(
    user_id: str,
    page: int = 1,
    per_page: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """
    List user's image analyses
    """
    try:
        # Calculate offset
        offset = (page - 1) * per_page
        
        # Get analyses
        stmt = (
            select(ImageAnalysis)
            .where(ImageAnalysis.user_id == user_id)
            .order_by(ImageAnalysis.created_at.desc())
            .offset(offset)
            .limit(per_page)
        )
        result = await db.execute(stmt)
        analyses = result.scalars().all()
        
        # Get total count
        count_stmt = select(ImageAnalysis).where(ImageAnalysis.user_id == user_id)
        count_result = await db.execute(count_stmt)
        total = len(count_result.scalars().all())
        
        # Convert to response models
        analysis_responses = []
        for analysis in analyses:
            response = ImageAnalysisResponse(
                analysis_id=analysis.id,
                status=AnalysisStatus(analysis.status),
                image_url=analysis.image_url,
                created_at=analysis.created_at,
                processing_time=analysis.processing_time,
                error_message=analysis.error_message if analysis.status == "failed" else None
            )
            analysis_responses.append(response)
        
        return ListAnalysesResponse(
            analyses=analysis_responses,
            total=total,
            page=page,
            per_page=per_page
        )
        
    except Exception as e:
        logger.error(f"Error listing analyses for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to list analyses")