"""
Chat service for handling conversation logic and AI responses
"""

import openai
from openai import AsyncOpenAI
from typing import List, Optional, Dict, Any
import logging
from dataclasses import dataclass

from core.config import settings
from schemas.chat import ChatMessage, MessageRole, UserContext

logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


@dataclass
class AIResponse:
    """AI response data class"""
    content: str
    next_question: Optional[str] = None
    metadata: Dict[str, Any] = None


class ChatService:
    """Service for handling chat conversations and AI responses"""
    
    def __init__(self):
        self.questions = [
            "What's the occasion you're dressing for? (e.g., work, date, casual outing, party)",
            "What's your preferred style? (e.g., minimalist, streetwear, classic, bohemian, edgy)",
            "Do you have any color preferences or colors you'd like to avoid?",
            "What's your budget range for this outfit? (e.g., $50-100, $100-200, $200+)"
        ]
        
        self.system_prompt = """
        You are StyleAI, a professional fashion consultant and personal stylist. Your role is to:
        
        1. Conduct a friendly, conversational interview to understand the user's style needs
        2. Ask follow-up questions to gather complete information about:
           - Occasion (work, casual, formal, date, party, etc.)
           - Style preference (minimalist, streetwear, classic, bohemian, edgy, etc.)
           - Color preferences or restrictions
           - Budget range
           - Any specific requirements or constraints
        
        3. Be conversational, warm, and encouraging
        4. Ask one question at a time to avoid overwhelming the user
        5. Acknowledge their responses and build on them
        6. Once you have enough information, let them know you're ready for the next step
        
        Keep responses concise but friendly. Use emojis sparingly and appropriately.
        """
    
    def get_initial_questions(self) -> List[str]:
        """Get the list of initial questions for the conversation"""
        return self.questions.copy()
    
    async def generate_response(
        self, 
        conversation_history: List[ChatMessage], 
        conversation_id: str
    ) -> AIResponse:
        """Generate AI response based on conversation history"""
        try:
            # Prepare messages for OpenAI
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Add conversation history
            for msg in conversation_history:
                messages.append({
                    "role": msg.role.value,
                    "content": msg.content
                })
            
            # Generate response using OpenAI
            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                max_tokens=300,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            ai_content = response.choices[0].message.content.strip()
            
            # Determine next question based on conversation progress
            next_question = self._get_next_question(conversation_history)
            
            return AIResponse(
                content=ai_content,
                next_question=next_question,
                metadata={
                    "model": settings.OPENAI_MODEL,
                    "tokens_used": response.usage.total_tokens
                }
            )
            
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            # Fallback response
            return AIResponse(
                content="I apologize, but I'm having trouble processing your request right now. Could you please try again?",
                next_question=None
            )
    
    def _get_next_question(self, conversation_history: List[ChatMessage]) -> Optional[str]:
        """Determine the next question to ask based on conversation progress"""
        user_messages = [msg for msg in conversation_history if msg.role == MessageRole.USER]
        
        # Simple logic to determine next question
        if len(user_messages) < len(self.questions):
            return self.questions[len(user_messages)]
        
        return None
    
    def is_conversation_complete(self, user_context: Dict[str, Any]) -> bool:
        """Check if the conversation has gathered enough information"""
        required_fields = [
            user_context.get('occasion'),
            user_context.get('style_preference'),
            user_context.get('budget')
        ]
        
        # At least 3 out of 4 main fields should be filled
        filled_fields = sum(1 for field in required_fields if field)
        return filled_fields >= 3
    
    def extract_context_from_message(self, message: str) -> Dict[str, Any]:
        """Extract context information from a user message"""
        context = {}
        message_lower = message.lower()
        
        # Extract occasion
        occasions = {
            'work': ['work', 'office', 'professional', 'business', 'meeting'],
            'casual': ['casual', 'everyday', 'relaxed', 'comfortable'],
            'date': ['date', 'romantic', 'dinner'],
            'party': ['party', 'celebration', 'event', 'festive'],
            'formal': ['formal', 'elegant', 'sophisticated', 'dressy']
        }
        
        for occasion, keywords in occasions.items():
            if any(keyword in message_lower for keyword in keywords):
                context['occasion'] = occasion
                break
        
        # Extract style preferences
        styles = {
            'minimalist': ['minimalist', 'simple', 'clean', 'minimal'],
            'streetwear': ['streetwear', 'urban', 'street', 'hip hop'],
            'classic': ['classic', 'traditional', 'timeless', 'conservative'],
            'bohemian': ['bohemian', 'boho', 'free-spirited', 'artistic'],
            'edgy': ['edgy', 'bold', 'alternative', 'punk', 'rock']
        }
        
        for style, keywords in styles.items():
            if any(keyword in message_lower for keyword in keywords):
                context['style_preference'] = style
                break
        
        # Extract budget (simple pattern matching)
        import re
        budget_pattern = r'\$(\d+)[-\s]*(\d+)?'
        budget_match = re.search(budget_pattern, message)
        if budget_match:
            min_price = budget_match.group(1)
            max_price = budget_match.group(2) if budget_match.group(2) else None
            if max_price:
                context['budget'] = f"${min_price}-{max_price}"
            else:
                context['budget'] = f"${min_price}+"
        
        return context