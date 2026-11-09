from typing import List, Optional
from pydantic import BaseModel, Field


class ResourceItem(BaseModel):
    id: str
    title: str
    description: str
    url: str
    provider: str  # Coursera, freeCodeCamp, Official Docs, YouTube, etc.
    type: str  # course, documentation, video, article, practice
    skill_tags: List[str] = Field(default_factory=list)
    difficulty: str = "all_levels"  # beginner, intermediate, advanced, all_levels
    estimated_hours: Optional[int] = None
    is_free: bool = True


class ResourceListResponse(BaseModel):
    total: int
    items: List[ResourceItem]

