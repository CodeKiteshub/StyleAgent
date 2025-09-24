"""
User-related Pydantic schemas
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class BodyType(str, Enum):
    """Body type enumeration"""
    RECTANGLE = "rectangle"
    PEAR = "pear"
    APPLE = "apple"
    HOURGLASS = "hourglass"
    INVERTED_TRIANGLE = "inverted_triangle"


class AccountStatus(str, Enum):
    """Account status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"


# Authentication schemas
class UserRegistration(BaseModel):
    """User registration request"""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    full_name: str = Field(..., min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=13, le=120)
    
    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserLogin(BaseModel):
    """User login request"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Authentication token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str


# User profile schemas
class UserPreferences(BaseModel):
    """User style preferences"""
    style_preference: Optional[str] = Field(None, description="Primary style preference")
    preferred_colors: Optional[List[str]] = Field(default_factory=list)
    budget_range: Optional[str] = Field(None, description="Budget range preference")
    body_type: Optional[BodyType] = None
    size_preferences: Optional[Dict[str, str]] = Field(default_factory=dict)
    occasion_preferences: Optional[List[str]] = Field(default_factory=list)


class UserProfileUpdate(BaseModel):
    """User profile update request"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=13, le=120)
    location: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    preferences: Optional[UserPreferences] = None


class UserProfile(BaseModel):
    """User profile response"""
    user_id: str
    email: str
    full_name: str
    age: Optional[int]
    location: Optional[str]
    bio: Optional[str]
    
    # Style preferences
    style_preference: Optional[str]
    preferred_colors: List[str]
    budget_range: Optional[str]
    body_type: Optional[BodyType]
    size_preferences: Dict[str, str]
    occasion_preferences: List[str]
    
    # Account info
    account_status: AccountStatus
    email_verified: bool
    created_at: datetime
    last_active: Optional[datetime]
    
    # Statistics
    total_conversations: int = 0
    total_recommendations: int = 0
    
    class Config:
        from_attributes = True


class UserSummary(BaseModel):
    """Simplified user summary"""
    user_id: str
    full_name: str
    email: str
    account_status: AccountStatus
    created_at: datetime
    last_active: Optional[datetime]


class UserListResponse(BaseModel):
    """User list response"""
    users: List[UserSummary]
    total_count: int
    page: int
    page_size: int


# Password management
class PasswordChangeRequest(BaseModel):
    """Password change request"""
    current_password: str
    new_password: str = Field(..., min_length=8)
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class PasswordResetRequest(BaseModel):
    """Password reset request"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation"""
    token: str
    new_password: str = Field(..., min_length=8)
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


# Email verification
class EmailVerificationRequest(BaseModel):
    """Email verification request"""
    email: EmailStr


class EmailVerificationConfirm(BaseModel):
    """Email verification confirmation"""
    token: str


# User activity and analytics
class UserActivity(BaseModel):
    """User activity data"""
    user_id: str
    activity_type: str
    activity_data: Dict[str, Any]
    timestamp: datetime


class UserAnalytics(BaseModel):
    """User analytics summary"""
    user_id: str
    total_conversations: int
    total_messages: int
    total_image_analyses: int
    total_recommendations_received: int
    total_recommendations_liked: int
    total_recommendations_saved: int
    engagement_rate: float
    favorite_styles: List[str]
    favorite_colors: List[str]
    most_common_occasions: List[str]
    created_at: datetime
    last_updated: datetime


# Admin schemas
class UserAdminUpdate(BaseModel):
    """Admin user update"""
    account_status: Optional[AccountStatus] = None
    email_verified: Optional[bool] = None
    notes: Optional[str] = Field(None, max_length=1000)


class BulkUserAction(BaseModel):
    """Bulk user action request"""
    user_ids: List[str]
    action: str  # 'activate', 'deactivate', 'suspend', 'delete'
    reason: Optional[str] = Field(None, max_length=500)


# Response schemas
class UserCreationResponse(BaseModel):
    """User creation response"""
    user_id: str
    email: str
    full_name: str
    account_status: AccountStatus
    message: str


class UserUpdateResponse(BaseModel):
    """User update response"""
    user_id: str
    message: str
    updated_fields: List[str]


class UserDeletionResponse(BaseModel):
    """User deletion response"""
    user_id: str
    message: str
    deleted_at: datetime


# Preferences and settings
class NotificationSettings(BaseModel):
    """User notification settings"""
    email_notifications: bool = True
    push_notifications: bool = True
    marketing_emails: bool = False
    trend_alerts: bool = True
    recommendation_updates: bool = True


class PrivacySettings(BaseModel):
    """User privacy settings"""
    profile_visibility: str = "public"  # public, friends, private
    data_sharing: bool = False
    analytics_tracking: bool = True
    personalized_ads: bool = True


class UserSettings(BaseModel):
    """Complete user settings"""
    notifications: NotificationSettings
    privacy: PrivacySettings
    language: str = "en"
    timezone: str = "UTC"
    theme: str = "light"  # light, dark, auto


class UserSettingsUpdate(BaseModel):
    """User settings update request"""
    notifications: Optional[NotificationSettings] = None
    privacy: Optional[PrivacySettings] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    theme: Optional[str] = None