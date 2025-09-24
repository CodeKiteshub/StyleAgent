"""
Pydantic schemas for chat API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """Message role enumeration"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    """Chat message schema"""
    role: MessageRole
    content: str
    metadata: Optional[Dict[str, Any]] = {}


class StartChatRequest(BaseModel):
    """Request to start a new chat session"""
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    initial_message: Optional[str] = None


class StartChatResponse(BaseModel):
    """Response for starting a new chat session"""
    conversation_id: str
    session_id: str
    message: str
    questions: List[str]


class SendMessageRequest(BaseModel):
    """Request to send a message in a conversation"""
    conversation_id: str
    message: str
    user_id: Optional[str] = None


class SendMessageResponse(BaseModel):
    """Response for sending a message"""
    message_id: str
    response: str
    conversation_status: str
    user_context: Optional[Dict[str, Any]] = {}
    next_question: Optional[str] = None
    is_complete: bool = False


class UserContext(BaseModel):
    """User context extracted from conversation"""
    occasion: Optional[str] = None
    style_preference: Optional[str] = None
    color_preference: Optional[str] = None
    budget: Optional[str] = None
    body_type: Optional[str] = None
    additional_context: Optional[Dict[str, Any]] = {}


class ConversationHistory(BaseModel):
    """Conversation history schema"""
    conversation_id: str
    user_id: Optional[str] = None
    status: str
    messages: List[ChatMessage]
    user_context: Optional[UserContext] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class GetConversationResponse(BaseModel):
    """Response for getting conversation details"""
    conversation: ConversationHistory


class ConversationSummary(BaseModel):
    """Summary of a conversation"""
    conversation_id: str
    status: str
    message_count: int
    last_message: Optional[str] = None
    user_context: Optional[UserContext] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class ListConversationsResponse(BaseModel):
    """Response for listing conversations"""
    conversations: List[ConversationSummary]
    total: int
    page: int = 1
    per_page: int = 10


class CompleteConversationRequest(BaseModel):
    """Request to mark conversation as complete"""
    conversation_id: str
    final_context: Optional[UserContext] = None


class CompleteConversationResponse(BaseModel):
    """Response for completing a conversation"""
    conversation_id: str
    status: str
    user_context: UserContext
    message: str