"""
Chat API routes for StyleAgent
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional
import uuid
import logging

from core.database import get_db
from models.conversation import Conversation, Message, ConversationStatus, MessageRole
from models.user import User
from schemas.chat import (
    StartChatRequest, StartChatResponse, SendMessageRequest, SendMessageResponse,
    GetConversationResponse, ListConversationsResponse, CompleteConversationRequest,
    CompleteConversationResponse, UserContext, ChatMessage, ConversationHistory
)
from services.chat_service import ChatService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/conversations", response_model=StartChatResponse)
async def create_conversation(
    request: dict = {},
    db: AsyncSession = Depends(get_db)
):
    """Create a new chat conversation"""
    # Temporary mock response to test routing
    conversation_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())
    
    response = StartChatResponse(
        conversation_id=conversation_id,
        session_id=session_id,
        message="Hi! I'm StyleAI, your personal fashion consultant. I'll help you find the perfect outfit!",
        questions=[
            "What's the occasion you're dressing for?",
            "What's your preferred style?",
            "Do you have any color preferences?",
            "What's your budget range for this outfit?"
        ]
    )
    
    return response


@router.post("/start", response_model=StartChatResponse)
async def start_chat(
    request: StartChatRequest,
    db: AsyncSession = Depends(get_db)
):
    """Start a new chat conversation"""
    try:
        # Create or get user
        user_id = request.user_id or str(uuid.uuid4())
        
        # Check if user exists, create if not
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            user = User(id=user_id)
            db.add(user)
            await db.commit()
        
        # Create new conversation
        conversation = Conversation(
            user_id=user_id,
            session_id=request.session_id or str(uuid.uuid4()),
            status=ConversationStatus.ACTIVE
        )
        db.add(conversation)
        await db.flush()
        
        # Initialize chat service
        chat_service = ChatService()
        
        # Get initial questions
        initial_questions = chat_service.get_initial_questions()
        
        # Create initial system message
        initial_message = (
            "Hi! I'm StyleAI, your personal fashion consultant. "
            "I'll help you find the perfect outfit by understanding your style preferences, "
            "occasion, and personal taste. Let's start with a few questions!"
        )
        
        # Add initial message to conversation
        message = Message(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=initial_message,
            sequence_number=1
        )
        db.add(message)
        
        # If user provided initial message, add it
        if request.initial_message:
            user_message = Message(
                conversation_id=conversation.id,
                role=MessageRole.USER,
                content=request.initial_message,
                sequence_number=2
            )
            db.add(user_message)
        
        await db.commit()
        
        return StartChatResponse(
            conversation_id=conversation.id,
            session_id=conversation.session_id,
            message=initial_message,
            questions=initial_questions
        )
        
    except Exception as e:
        logger.error(f"Error starting chat: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start chat session"
        )


@router.post("/message", response_model=SendMessageResponse)
async def send_message(
    request: SendMessageRequest,
    db: AsyncSession = Depends(get_db)
):
    """Send a message in an existing conversation"""
    try:
        # Get conversation
        result = await db.execute(
            select(Conversation).where(Conversation.id == request.conversation_id)
        )
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        if conversation.status != ConversationStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Conversation is not active"
            )
        
        # Get current message count for sequence number
        result = await db.execute(
            select(Message).where(Message.conversation_id == conversation.id)
        )
        messages = result.scalars().all()
        next_sequence = len(messages) + 1
        
        # Add user message
        user_message = Message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=request.message,
            sequence_number=next_sequence
        )
        db.add(user_message)
        
        # Initialize services
        chat_service = ChatService()
        
        # Get conversation history
        conversation_messages = [
            ChatMessage(role=MessageRole(msg.role), content=msg.content)
            for msg in sorted(messages, key=lambda x: x.sequence_number)
        ]
        conversation_messages.append(
            ChatMessage(role=MessageRole.USER, content=request.message)
        )
        
        # Generate AI response
        ai_response = await chat_service.generate_response(
            conversation_messages, conversation.id
        )
        
        # Add AI response message
        ai_message = Message(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=ai_response.content,
            sequence_number=next_sequence + 1
        )
        db.add(ai_message)
        
        # Extract user context from the latest message
        extracted_context = chat_service.extract_context_from_message(request.message)
        
        # Update conversation with extracted context
        if extracted_context.get('occasion'):
            conversation.occasion = extracted_context['occasion']
        if extracted_context.get('style_preference'):
            conversation.style_preference = extracted_context['style_preference']
        if extracted_context.get('color_preference'):
            conversation.color_preference = extracted_context['color_preference']
        if extracted_context.get('budget'):
            conversation.budget = extracted_context['budget']
        
        # Check if conversation is complete
        is_complete = chat_service.is_conversation_complete(extracted_context)
        
        if is_complete:
            conversation.status = ConversationStatus.COMPLETED
        
        await db.commit()
        
        return SendMessageResponse(
            message_id=ai_message.id,
            response=ai_response.content,
            conversation_status=conversation.status.value,
            user_context=extracted_context,
            next_question=ai_response.next_question,
            is_complete=is_complete
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send message"
        )


@router.get("/{conversation_id}", response_model=GetConversationResponse)
async def get_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get conversation details and history"""
    try:
        # Get conversation with messages
        result = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Get messages
        result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.sequence_number)
        )
        messages = result.scalars().all()
        
        # Convert to schema
        chat_messages = [
            ChatMessage(
                role=MessageRole(msg.role),
                content=msg.content
            )
            for msg in messages
        ]
        
        user_context = UserContext(
            occasion=conversation.occasion,
            style_preference=conversation.style_preference,
            color_preference=conversation.color_preference,
            budget=conversation.budget,
            additional_context=conversation.additional_context or {}
        )
        
        conversation_history = ConversationHistory(
            conversation_id=conversation.id,
            user_id=conversation.user_id,
            status=conversation.status.value,
            messages=chat_messages,
            user_context=user_context,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at
        )
        
        return GetConversationResponse(conversation=conversation_history)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get conversation"
        )


@router.get("/user/{user_id}/conversations")
async def list_user_conversations(
    user_id: str,
    page: int = 1,
    per_page: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """List conversations for a user"""
    try:
        offset = (page - 1) * per_page
        
        # Get conversations
        result = await db.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .offset(offset)
            .limit(per_page)
        )
        conversations = result.scalars().all()
        
        # Get total count
        count_result = await db.execute(
            select(Conversation).where(Conversation.user_id == user_id)
        )
        total = len(count_result.scalars().all())
        
        return ListConversationsResponse(
            conversations=[conv.to_dict() for conv in conversations],
            total=total,
            page=page,
            per_page=per_page
        )
        
    except Exception as e:
        logger.error(f"Error listing conversations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list conversations"
        )


@router.post("/complete", response_model=CompleteConversationResponse)
async def complete_conversation(
    request: CompleteConversationRequest,
    db: AsyncSession = Depends(get_db)
):
    """Mark a conversation as complete"""
    try:
        # Get conversation
        result = await db.execute(
            select(Conversation).where(Conversation.id == request.conversation_id)
        )
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Update conversation status
        conversation.status = ConversationStatus.COMPLETED
        
        # Update context if provided
        if request.final_context:
            if request.final_context.occasion:
                conversation.occasion = request.final_context.occasion
            if request.final_context.style_preference:
                conversation.style_preference = request.final_context.style_preference
            if request.final_context.color_preference:
                conversation.color_preference = request.final_context.color_preference
            if request.final_context.budget:
                conversation.budget = request.final_context.budget
        
        await db.commit()
        
        user_context = UserContext(
            occasion=conversation.occasion,
            style_preference=conversation.style_preference,
            color_preference=conversation.color_preference,
            budget=conversation.budget,
            additional_context=conversation.additional_context or {}
        )
        
        return CompleteConversationResponse(
            conversation_id=conversation.id,
            status=conversation.status.value,
            user_context=user_context,
            message="Conversation completed successfully. Ready for outfit recommendations!"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error completing conversation: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to complete conversation"
        )