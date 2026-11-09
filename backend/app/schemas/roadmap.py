from typing import List, Optional
from pydantic import BaseModel, Field


class RoadmapResource(BaseModel):
    title: str
    url: Optional[str] = None
    type: str = "article"  # article, video, course, documentation


class RoadmapMilestone(BaseModel):
    id: str
    title: str
    description: str
    estimated_hours: int = 10
    skills_covered: List[str] = Field(default_factory=list)
    resources: List[RoadmapResource] = Field(default_factory=list)
    is_completed: bool = False


class RoadmapPhase(BaseModel):
    phase_number: int
    title: str
    description: str
    milestones: List[RoadmapMilestone] = Field(default_factory=list)


class RoadmapCreateRequest(BaseModel):
    target_role: str = Field(..., min_length=2, max_length=100, example="Full Stack Developer")
    current_level: str = Field(default="beginner", example="beginner")  # beginner, intermediate, advanced, changer
    hours_per_week: int = Field(default=10, ge=1, le=80, example=15)
    background: Optional[str] = Field(default=None, example="Computer Science student with Python basics")
    preferred_learning_style: Optional[str] = Field(default="hands_on", example="hands_on")


class RoadmapResponse(BaseModel):
    id: str
    target_role: str
    current_level: str
    estimated_weeks: int
    summary: str
    phases: List[RoadmapPhase]
    total_milestones: int
    completed_milestones: int


class MilestoneUpdateRequest(BaseModel):
    is_completed: bool

