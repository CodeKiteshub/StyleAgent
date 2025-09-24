"""
User management service
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, and_, or_
from sqlalchemy.orm import selectinload

from models.user import User
from models.conversation import Conversation
from models.image_analysis import ImageAnalysis
from models.outfit import OutfitRecommendation
from schemas.user import (
    UserRegistration, UserProfile, UserProfileUpdate, UserPreferences,
    UserActivity, UserAnalytics, UserSettings
)
from services.auth_service import AuthService

logger = logging.getLogger(__name__)


class UserService:
    """Service for user management operations"""
    
    def __init__(self):
        self.auth_service = AuthService()
    
    async def create_user(self, db: AsyncSession, user_data: UserRegistration) -> Optional[User]:
        """Create a new user"""
        try:
            # Check if user already exists
            existing_user = await self.get_user_by_email(db, user_data.email)
            if existing_user:
                logger.warning(f"User with email {user_data.email} already exists")
                return None
            
            # Hash password
            hashed_password = self.auth_service.hash_password(user_data.password)
            
            # Create user
            user = User(
                email=user_data.email,
                password_hash=hashed_password,
                full_name=user_data.full_name,
                date_of_birth=user_data.date_of_birth,
                gender=user_data.gender,
                phone_number=user_data.phone_number,
                preferred_style=user_data.preferred_style,
                body_type=user_data.body_type,
                preferred_colors=user_data.preferred_colors or [],
                budget_range_min=user_data.budget_range_min,
                budget_range_max=user_data.budget_range_max,
                location=user_data.location,
                account_status="pending_verification",
                email_verified=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.add(user)
            await db.commit()
            await db.refresh(user)
            
            logger.info(f"Created user with ID: {user.id}")
            return user
            
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            await db.rollback()
            return None
    
    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            result = await db.execute(
                select(User).where(User.id == user_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting user by ID {user_id}: {e}")
            return None
    
    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            result = await db.execute(
                select(User).where(User.email == email)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            return None
    
    async def authenticate_user(self, db: AsyncSession, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        try:
            user = await self.get_user_by_email(db, email)
            if not user:
                return None
            
            if not self.auth_service.verify_password(password, user.password_hash):
                return None
            
            # Update last login
            user.last_login = datetime.utcnow()
            await db.commit()
            
            return user
            
        except Exception as e:
            logger.error(f"Error authenticating user {email}: {e}")
            return None
    
    async def update_user_profile(self, db: AsyncSession, user_id: int, update_data: UserProfileUpdate) -> Optional[User]:
        """Update user profile"""
        try:
            user = await self.get_user_by_id(db, user_id)
            if not user:
                return None
            
            # Update fields if provided
            update_dict = update_data.dict(exclude_unset=True)
            
            for field, value in update_dict.items():
                if hasattr(user, field):
                    setattr(user, field, value)
            
            user.updated_at = datetime.utcnow()
            
            await db.commit()
            await db.refresh(user)
            
            logger.info(f"Updated user profile for user ID: {user_id}")
            return user
            
        except Exception as e:
            logger.error(f"Error updating user profile {user_id}: {e}")
            await db.rollback()
            return None
    
    async def verify_email(self, db: AsyncSession, email: str) -> bool:
        """Mark user email as verified"""
        try:
            result = await db.execute(
                update(User)
                .where(User.email == email)
                .values(
                    email_verified=True,
                    account_status="active",
                    updated_at=datetime.utcnow()
                )
            )
            
            await db.commit()
            
            if result.rowcount > 0:
                logger.info(f"Email verified for user: {email}")
                return True
            else:
                logger.warning(f"No user found with email: {email}")
                return False
                
        except Exception as e:
            logger.error(f"Error verifying email {email}: {e}")
            await db.rollback()
            return False
    
    async def update_password(self, db: AsyncSession, user_id: int, new_password: str) -> bool:
        """Update user password"""
        try:
            hashed_password = self.auth_service.hash_password(new_password)
            
            result = await db.execute(
                update(User)
                .where(User.id == user_id)
                .values(
                    password_hash=hashed_password,
                    updated_at=datetime.utcnow()
                )
            )
            
            await db.commit()
            
            if result.rowcount > 0:
                logger.info(f"Password updated for user ID: {user_id}")
                return True
            else:
                logger.warning(f"No user found with ID: {user_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating password for user {user_id}: {e}")
            await db.rollback()
            return False
    
    async def reset_password_by_email(self, db: AsyncSession, email: str, new_password: str) -> bool:
        """Reset password by email (for password reset flow)"""
        try:
            hashed_password = self.auth_service.hash_password(new_password)
            
            result = await db.execute(
                update(User)
                .where(User.email == email)
                .values(
                    password_hash=hashed_password,
                    updated_at=datetime.utcnow()
                )
            )
            
            await db.commit()
            
            if result.rowcount > 0:
                logger.info(f"Password reset for user: {email}")
                return True
            else:
                logger.warning(f"No user found with email: {email}")
                return False
                
        except Exception as e:
            logger.error(f"Error resetting password for email {email}: {e}")
            await db.rollback()
            return False
    
    async def deactivate_user(self, db: AsyncSession, user_id: int) -> bool:
        """Deactivate user account"""
        try:
            result = await db.execute(
                update(User)
                .where(User.id == user_id)
                .values(
                    account_status="inactive",
                    updated_at=datetime.utcnow()
                )
            )
            
            await db.commit()
            
            if result.rowcount > 0:
                logger.info(f"User deactivated: {user_id}")
                return True
            else:
                logger.warning(f"No user found with ID: {user_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error deactivating user {user_id}: {e}")
            await db.rollback()
            return False
    
    async def delete_user(self, db: AsyncSession, user_id: int) -> bool:
        """Delete user account (soft delete by marking as deleted)"""
        try:
            result = await db.execute(
                update(User)
                .where(User.id == user_id)
                .values(
                    account_status="deleted",
                    updated_at=datetime.utcnow()
                )
            )
            
            await db.commit()
            
            if result.rowcount > 0:
                logger.info(f"User deleted: {user_id}")
                return True
            else:
                logger.warning(f"No user found with ID: {user_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            await db.rollback()
            return False
    
    async def get_user_activity(self, db: AsyncSession, user_id: int, days: int = 30) -> UserActivity:
        """Get user activity statistics"""
        try:
            since_date = datetime.utcnow() - timedelta(days=days)
            
            # Get conversation count
            conversations_result = await db.execute(
                select(func.count(Conversation.id))
                .where(
                    and_(
                        Conversation.user_id == user_id,
                        Conversation.created_at >= since_date
                    )
                )
            )
            conversations_count = conversations_result.scalar() or 0
            
            # Get image analysis count
            analyses_result = await db.execute(
                select(func.count(ImageAnalysis.id))
                .where(
                    and_(
                        ImageAnalysis.user_id == user_id,
                        ImageAnalysis.created_at >= since_date
                    )
                )
            )
            analyses_count = analyses_result.scalar() or 0
            
            # Get recommendations count
            recommendations_result = await db.execute(
                select(func.count(OutfitRecommendation.id))
                .where(
                    and_(
                        OutfitRecommendation.user_id == user_id,
                        OutfitRecommendation.created_at >= since_date
                    )
                )
            )
            recommendations_count = recommendations_result.scalar() or 0
            
            # Get last login
            user = await self.get_user_by_id(db, user_id)
            last_login = user.last_login if user else None
            
            return UserActivity(
                user_id=user_id,
                conversations_count=conversations_count,
                images_analyzed=analyses_count,
                recommendations_received=recommendations_count,
                last_login=last_login,
                period_days=days
            )
            
        except Exception as e:
            logger.error(f"Error getting user activity for user {user_id}: {e}")
            return UserActivity(
                user_id=user_id,
                conversations_count=0,
                images_analyzed=0,
                recommendations_received=0,
                last_login=None,
                period_days=days
            )
    
    async def get_user_analytics(self, db: AsyncSession, user_id: int) -> UserAnalytics:
        """Get comprehensive user analytics"""
        try:
            user = await self.get_user_by_id(db, user_id)
            if not user:
                return None
            
            # Get total counts
            total_conversations = await db.execute(
                select(func.count(Conversation.id))
                .where(Conversation.user_id == user_id)
            )
            total_conversations_count = total_conversations.scalar() or 0
            
            total_analyses = await db.execute(
                select(func.count(ImageAnalysis.id))
                .where(ImageAnalysis.user_id == user_id)
            )
            total_analyses_count = total_analyses.scalar() or 0
            
            total_recommendations = await db.execute(
                select(func.count(OutfitRecommendation.id))
                .where(OutfitRecommendation.user_id == user_id)
            )
            total_recommendations_count = total_recommendations.scalar() or 0
            
            # Get favorite styles (from recommendations)
            favorite_styles_result = await db.execute(
                select(OutfitRecommendation.style_match_percentage, func.count())
                .where(OutfitRecommendation.user_id == user_id)
                .group_by(OutfitRecommendation.style_match_percentage)
                .order_by(func.count().desc())
                .limit(5)
            )
            favorite_styles = [row[0] for row in favorite_styles_result.fetchall()]
            
            # Calculate engagement score (simple formula)
            days_since_registration = (datetime.utcnow() - user.created_at).days or 1
            engagement_score = min(100, (
                (total_conversations_count * 10 + 
                 total_analyses_count * 5 + 
                 total_recommendations_count * 2) / days_since_registration
            ) * 10)
            
            return UserAnalytics(
                user_id=user_id,
                total_conversations=total_conversations_count,
                total_images_analyzed=total_analyses_count,
                total_recommendations=total_recommendations_count,
                favorite_styles=favorite_styles,
                engagement_score=round(engagement_score, 2),
                account_age_days=days_since_registration,
                last_active=user.last_login
            )
            
        except Exception as e:
            logger.error(f"Error getting user analytics for user {user_id}: {e}")
            return None
    
    async def update_user_preferences(self, db: AsyncSession, user_id: int, preferences: UserPreferences) -> bool:
        """Update user preferences"""
        try:
            update_data = {
                "preferred_style": preferences.preferred_style,
                "body_type": preferences.body_type,
                "preferred_colors": preferences.preferred_colors,
                "budget_range_min": preferences.budget_range_min,
                "budget_range_max": preferences.budget_range_max,
                "updated_at": datetime.utcnow()
            }
            
            result = await db.execute(
                update(User)
                .where(User.id == user_id)
                .values(**update_data)
            )
            
            await db.commit()
            
            if result.rowcount > 0:
                logger.info(f"Preferences updated for user ID: {user_id}")
                return True
            else:
                logger.warning(f"No user found with ID: {user_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating preferences for user {user_id}: {e}")
            await db.rollback()
            return False
    
    async def get_users_list(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100,
        status_filter: Optional[str] = None,
        search_query: Optional[str] = None
    ) -> List[User]:
        """Get list of users with filtering and pagination"""
        try:
            query = select(User)
            
            # Apply filters
            if status_filter:
                query = query.where(User.account_status == status_filter)
            
            if search_query:
                search_pattern = f"%{search_query}%"
                query = query.where(
                    or_(
                        User.full_name.ilike(search_pattern),
                        User.email.ilike(search_pattern)
                    )
                )
            
            # Apply pagination
            query = query.offset(skip).limit(limit)
            query = query.order_by(User.created_at.desc())
            
            result = await db.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            logger.error(f"Error getting users list: {e}")
            return []
    
    async def get_users_count(
        self, 
        db: AsyncSession,
        status_filter: Optional[str] = None
    ) -> int:
        """Get total count of users"""
        try:
            query = select(func.count(User.id))
            
            if status_filter:
                query = query.where(User.account_status == status_filter)
            
            result = await db.execute(query)
            return result.scalar() or 0
            
        except Exception as e:
            logger.error(f"Error getting users count: {e}")
            return 0
    
    def convert_to_profile(self, user: User) -> UserProfile:
        """Convert User model to UserProfile schema"""
        return UserProfile(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            date_of_birth=user.date_of_birth,
            gender=user.gender,
            phone_number=user.phone_number,
            preferred_style=user.preferred_style,
            body_type=user.body_type,
            preferred_colors=user.preferred_colors or [],
            budget_range_min=user.budget_range_min,
            budget_range_max=user.budget_range_max,
            location=user.location,
            profile_image_url=user.profile_image_url,
            bio=user.bio,
            account_status=user.account_status,
            email_verified=user.email_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login
        )