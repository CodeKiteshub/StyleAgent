"""
Authentication and user management service
"""

import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import secrets
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

from core.config import settings
from schemas.user import UserRegistration, UserLogin, TokenResponse
from models.user import User

logger = logging.getLogger(__name__)


class AuthService:
    """Service for authentication and user management"""
    
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = "HS256"
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = 30
        
        # Password hashing
        self.pwd_context = bcrypt
    
    def hash_password(self, password: str) -> str:
        """Hash a password"""
        try:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            logger.error(f"Error hashing password: {e}")
            raise
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'), 
                hashed_password.encode('utf-8')
            )
        except Exception as e:
            logger.error(f"Error verifying password: {e}")
            return False
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create JWT access token"""
        try:
            to_encode = data.copy()
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
            to_encode.update({"exp": expire, "type": "access"})
            
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            return encoded_jwt
        except Exception as e:
            logger.error(f"Error creating access token: {e}")
            raise
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create JWT refresh token"""
        try:
            to_encode = data.copy()
            expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
            to_encode.update({"exp": expire, "type": "refresh"})
            
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            return encoded_jwt
        except Exception as e:
            logger.error(f"Error creating refresh token: {e}")
            raise
    
    def verify_token(self, token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Check token type
            if payload.get("type") != token_type:
                return None
            
            # Check expiration
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
                return None
            
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.JWTError as e:
            logger.warning(f"JWT error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            return None
    
    def generate_verification_token(self, email: str) -> str:
        """Generate email verification token"""
        try:
            data = {
                "email": email,
                "purpose": "email_verification",
                "exp": datetime.utcnow() + timedelta(hours=24)
            }
            return jwt.encode(data, self.secret_key, algorithm=self.algorithm)
        except Exception as e:
            logger.error(f"Error generating verification token: {e}")
            raise
    
    def generate_reset_token(self, email: str) -> str:
        """Generate password reset token"""
        try:
            data = {
                "email": email,
                "purpose": "password_reset",
                "exp": datetime.utcnow() + timedelta(hours=1)
            }
            return jwt.encode(data, self.secret_key, algorithm=self.algorithm)
        except Exception as e:
            logger.error(f"Error generating reset token: {e}")
            raise
    
    def verify_verification_token(self, token: str, purpose: str) -> Optional[str]:
        """Verify email verification or password reset token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            if payload.get("purpose") != purpose:
                return None
            
            return payload.get("email")
        except jwt.ExpiredSignatureError:
            logger.warning("Verification token has expired")
            return None
        except jwt.JWTError as e:
            logger.warning(f"JWT error in verification token: {e}")
            return None
        except Exception as e:
            logger.error(f"Error verifying verification token: {e}")
            return None
    
    async def send_verification_email(self, email: str, token: str) -> bool:
        """Send email verification email"""
        try:
            # In production, use a proper email service like SendGrid, AWS SES, etc.
            # For now, we'll just log the verification link
            
            verification_link = f"{settings.FRONTEND_URL}/verify-email?token={token}"
            
            logger.info(f"Email verification link for {email}: {verification_link}")
            
            # Mock email sending
            if settings.SMTP_HOST and settings.SMTP_PORT:
                try:
                    msg = MIMEMultipart()
                    msg['From'] = settings.SMTP_USERNAME
                    msg['To'] = email
                    msg['Subject'] = "Verify Your StyleAgent Account"
                    
                    body = f"""
                    Welcome to StyleAgent!
                    
                    Please click the link below to verify your email address:
                    {verification_link}
                    
                    This link will expire in 24 hours.
                    
                    If you didn't create an account, please ignore this email.
                    
                    Best regards,
                    The StyleAgent Team
                    """
                    
                    msg.attach(MIMEText(body, 'plain'))
                    
                    server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
                    server.starttls()
                    server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                    text = msg.as_string()
                    server.sendmail(settings.SMTP_USERNAME, email, text)
                    server.quit()
                    
                    return True
                except Exception as e:
                    logger.error(f"Error sending email: {e}")
                    return False
            else:
                # Mock success for development
                return True
                
        except Exception as e:
            logger.error(f"Error in send_verification_email: {e}")
            return False
    
    async def send_password_reset_email(self, email: str, token: str) -> bool:
        """Send password reset email"""
        try:
            reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
            
            logger.info(f"Password reset link for {email}: {reset_link}")
            
            # Mock email sending (similar to verification email)
            if settings.SMTP_HOST and settings.SMTP_PORT:
                try:
                    msg = MIMEMultipart()
                    msg['From'] = settings.SMTP_USERNAME
                    msg['To'] = email
                    msg['Subject'] = "Reset Your StyleAgent Password"
                    
                    body = f"""
                    You requested a password reset for your StyleAgent account.
                    
                    Please click the link below to reset your password:
                    {reset_link}
                    
                    This link will expire in 1 hour.
                    
                    If you didn't request this reset, please ignore this email.
                    
                    Best regards,
                    The StyleAgent Team
                    """
                    
                    msg.attach(MIMEText(body, 'plain'))
                    
                    server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
                    server.starttls()
                    server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                    text = msg.as_string()
                    server.sendmail(settings.SMTP_USERNAME, email, text)
                    server.quit()
                    
                    return True
                except Exception as e:
                    logger.error(f"Error sending password reset email: {e}")
                    return False
            else:
                return True
                
        except Exception as e:
            logger.error(f"Error in send_password_reset_email: {e}")
            return False
    
    def generate_session_id(self) -> str:
        """Generate a secure session ID"""
        return secrets.token_urlsafe(32)
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """Validate password strength"""
        result = {
            "is_valid": True,
            "score": 0,
            "feedback": []
        }
        
        try:
            # Length check
            if len(password) < 8:
                result["is_valid"] = False
                result["feedback"].append("Password must be at least 8 characters long")
            else:
                result["score"] += 1
            
            # Uppercase check
            if not any(c.isupper() for c in password):
                result["is_valid"] = False
                result["feedback"].append("Password must contain at least one uppercase letter")
            else:
                result["score"] += 1
            
            # Lowercase check
            if not any(c.islower() for c in password):
                result["is_valid"] = False
                result["feedback"].append("Password must contain at least one lowercase letter")
            else:
                result["score"] += 1
            
            # Digit check
            if not any(c.isdigit() for c in password):
                result["is_valid"] = False
                result["feedback"].append("Password must contain at least one digit")
            else:
                result["score"] += 1
            
            # Special character check
            special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            if not any(c in special_chars for c in password):
                result["feedback"].append("Consider adding special characters for stronger security")
            else:
                result["score"] += 1
            
            # Length bonus
            if len(password) >= 12:
                result["score"] += 1
            
            # Common password check (simplified)
            common_passwords = [
                "password", "123456", "password123", "admin", "qwerty",
                "letmein", "welcome", "monkey", "dragon"
            ]
            if password.lower() in common_passwords:
                result["is_valid"] = False
                result["feedback"].append("This password is too common")
                result["score"] = 0
            
            return result
            
        except Exception as e:
            logger.error(f"Error validating password strength: {e}")
            return {
                "is_valid": False,
                "score": 0,
                "feedback": ["Error validating password"]
            }
    
    def create_token_response(self, user_data: Dict[str, Any]) -> TokenResponse:
        """Create token response with access and refresh tokens"""
        try:
            # Create access token
            access_token_data = {
                "sub": user_data["user_id"],
                "email": user_data["email"],
                "full_name": user_data.get("full_name", "")
            }
            access_token = self.create_access_token(access_token_data)
            
            # Create refresh token
            refresh_token_data = {
                "sub": user_data["user_id"],
                "email": user_data["email"]
            }
            refresh_token = self.create_refresh_token(refresh_token_data)
            
            return TokenResponse(
                access_token=access_token,
                token_type="bearer",
                expires_in=self.access_token_expire_minutes * 60,
                refresh_token=refresh_token
            )
            
        except Exception as e:
            logger.error(f"Error creating token response: {e}")
            raise
    
    def extract_user_from_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Extract user information from access token"""
        try:
            payload = self.verify_token(token, "access")
            if not payload:
                return None
            
            return {
                "user_id": payload.get("sub"),
                "email": payload.get("email"),
                "full_name": payload.get("full_name", "")
            }
            
        except Exception as e:
            logger.error(f"Error extracting user from token: {e}")
            return None
    
    def is_token_blacklisted(self, token: str) -> bool:
        """Check if token is blacklisted (for logout functionality)"""
        # In production, implement token blacklisting with Redis or database
        # For now, return False (no blacklisting)
        return False
    
    def blacklist_token(self, token: str) -> bool:
        """Add token to blacklist"""
        # In production, implement token blacklisting
        # For now, return True (mock success)
        return True