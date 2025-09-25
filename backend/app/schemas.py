from pydantic import BaseModel, Field
from typing import List, Optional


class SocialStats(BaseModel):
    likes: int
    shares: int


class OutfitRecommendation(BaseModel):
    id: str
    image_url: str
    title: str
    caption: str
    hashtags: List[str]
    price_range: str
    body_fit: str
    trend_score: int
    social_stats: SocialStats


class UserContext(BaseModel):
    occasion: Optional[str] = None
    style_preference: Optional[str] = None
    body_type: Optional[str] = None
    color_preference: Optional[str] = None
    budget: Optional[str] = None


class ChatMessage(BaseModel):
    role: str = Field(pattern="^(user|assistant|system)$")
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    reply: str
    user_context: UserContext


class AnalyzeRequest(BaseModel):
    image_base64: str
    user_context: UserContext


class AnalyzeResponse(BaseModel):
    analysis_summary: str
    detected_body_type: Optional[str] = None
    detected_style_cues: List[str] = []


class RecommendRequest(BaseModel):
    user_context: UserContext
    image_base64: Optional[str] = None


class RecommendResponse(BaseModel):
    recommendations: List[OutfitRecommendation]


