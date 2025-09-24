"""
User management API routes
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List, Optional
import logging

from core.database import get_db
from schemas.user import (
    UserProfile, UserProfileUpdate, UserPreferences, UserActivity, 
    UserAnalytics, UserSettings, PasswordChangeRequest,
    UserListResponse, UserSummary
)
from services.user_service import UserService
from services.auth_service import AuthService
from api.routes.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
user_service = UserService()
auth_service = AuthService()


@router.get("/profile", response_model=UserProfile)
async def get_user_profile(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get current user's profile"""
    try:
        user = current_user["user"]
        return user_service.convert_to_profile(user)
        
    except Exception as e:
        logger.error(f"Error getting user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user profile"
        )


@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get current user's profile - matches frontend GET /users/me call"""
    try:
        user = current_user["user"]
        return user_service.convert_to_profile(user)
        
    except Exception as e:
        logger.error(f"Error getting current user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user profile"
        )


@router.put("/profile", response_model=UserProfile)
async def update_user_profile(
    update_data: UserProfileUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user's profile"""
    try:
        user_id = current_user["user_id"]
        
        updated_user = await user_service.update_user_profile(db, user_id, update_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user_service.convert_to_profile(updated_user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile"
        )


@router.put("/preferences", response_model=Dict[str, str])
async def update_user_preferences(
    preferences: UserPreferences,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update user preferences"""
    try:
        user_id = current_user["user_id"]
        
        success = await user_service.update_user_preferences(db, user_id, preferences)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {"message": "Preferences updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user preferences: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update preferences"
        )


@router.post("/change-password", response_model=Dict[str, str])
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Change user password"""
    try:
        user_id = current_user["user_id"]
        user = current_user["user"]
        
        # Verify current password
        if not auth_service.verify_password(password_data.current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Validate new password strength
        password_validation = auth_service.validate_password_strength(password_data.new_password)
        if not password_validation["is_valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "New password does not meet requirements",
                    "feedback": password_validation["feedback"]
                }
            )
        
        # Update password
        success = await user_service.update_password(db, user_id, password_data.new_password)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update password"
            )
        
        logger.info(f"Password changed for user ID: {user_id}")
        return {"message": "Password changed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error changing password: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )


@router.get("/activity", response_model=UserActivity)
async def get_user_activity(
    days: int = Query(30, ge=1, le=365, description="Number of days to look back"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user activity statistics"""
    try:
        user_id = current_user["user_id"]
        
        activity = await user_service.get_user_activity(db, user_id, days)
        return activity
        
    except Exception as e:
        logger.error(f"Error getting user activity: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user activity"
        )


@router.get("/analytics", response_model=UserAnalytics)
async def get_user_analytics(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get comprehensive user analytics"""
    try:
        user_id = current_user["user_id"]
        
        analytics = await user_service.get_user_analytics(db, user_id)
        if not analytics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User analytics not found"
            )
        
        return analytics
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user analytics"
        )


@router.delete("/account", response_model=Dict[str, str])
async def deactivate_account(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Deactivate user account"""
    try:
        user_id = current_user["user_id"]
        
        success = await user_service.deactivate_user(db, user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"Account deactivated for user ID: {user_id}")
        return {"message": "Account deactivated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deactivating account: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to deactivate account"
        )


@router.delete("/account/permanent", response_model=Dict[str, str])
async def delete_account(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Permanently delete user account"""
    try:
        user_id = current_user["user_id"]
        
        success = await user_service.delete_user(db, user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"Account deleted for user ID: {user_id}")
        return {"message": "Account deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting account: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete account"
        )


# Admin routes (require admin privileges - simplified for now)
@router.get("/admin/list", response_model=UserListResponse)
async def list_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of users to return"),
    status_filter: Optional[str] = Query(None, description="Filter by account status"),
    search: Optional[str] = Query(None, description="Search by name or email"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List users (admin only)"""
    try:
        # In a real application, you would check if the user has admin privileges
        # For now, we'll allow any authenticated user to access this
        
        users = await user_service.get_users_list(
            db, skip=skip, limit=limit, 
            status_filter=status_filter, search_query=search
        )
        
        total_count = await user_service.get_users_count(db, status_filter)
        
        user_summaries = [
            UserSummary(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                account_status=user.account_status,
                email_verified=user.email_verified,
                created_at=user.created_at,
                last_login=user.last_login
            )
            for user in users
        ]
        
        return UserListResponse(
            users=user_summaries,
            total=total_count,
            skip=skip,
            limit=limit
        )
        
    except Exception as e:
        logger.error(f"Error listing users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list users"
        )


@router.get("/admin/{user_id}", response_model=UserProfile)
async def get_user_by_id(
    user_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user by ID (admin only)"""
    try:
        # In a real application, check admin privileges here
        
        user = await user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user_service.convert_to_profile(user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user by ID: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user"
        )


@router.put("/admin/{user_id}/status", response_model=Dict[str, str])
async def update_user_status(
    user_id: int,
    status_data: Dict[str, str],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update user account status (admin only)"""
    try:
        # In a real application, check admin privileges here
        
        new_status = status_data.get("status")
        if not new_status:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status is required"
            )
        
        user = await user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update status based on the new status
        if new_status == "inactive":
            success = await user_service.deactivate_user(db, user_id)
        elif new_status == "deleted":
            success = await user_service.delete_user(db, user_id)
        else:
            # For other statuses, update directly
            update_data = UserProfileUpdate(account_status=new_status)
            updated_user = await user_service.update_user_profile(db, user_id, update_data)
            success = updated_user is not None
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user status"
            )
        
        logger.info(f"User status updated for user ID {user_id} to {new_status}")
        return {"message": f"User status updated to {new_status.value}"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user status"
        )