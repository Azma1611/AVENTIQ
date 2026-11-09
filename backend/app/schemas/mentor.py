from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., example="user")  # "user", "assistant", "system"
    content: str
    timestamp: Optional[str] = None


class MentorContext(BaseModel):
    target_role: Optional[str] = None
    current_level: Optional[str] = None
    active_roadmap_id: Optional[str] = None
    current_milestone: Optional[str] = None


class MentorChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, example="How do I prepare for technical interviews for FastAPI backend roles?")
    conversation_id: Optional[str] = None
    context: Optional[MentorContext] = None


class MentorChatResponse(BaseModel):
    conversation_id: str
    reply: str
    actionable_tips: List[str] = Field(default_factory=list)
    suggested_prompts: List[str] = Field(default_factory=list)

