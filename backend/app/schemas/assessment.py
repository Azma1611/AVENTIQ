from typing import List, Optional
from pydantic import BaseModel, Field


class QuestionOption(BaseModel):
    id: str
    text: str


class AssessmentQuestion(BaseModel):
    id: str
    text: str
    category: str
    options: List[QuestionOption]
    difficulty: str = "medium"  # easy, medium, hard


class AssessmentStartRequest(BaseModel):
    domain: str = Field(..., min_length=2, max_length=100, example="Python Backend")
    target_role: Optional[str] = Field(default=None, example="Backend Engineer")
    skill_level: str = Field(default="beginner", example="beginner")


class AssessmentStartResponse(BaseModel):
    assessment_id: str
    domain: str
    total_questions: int
    questions: List[AssessmentQuestion]


class AssessmentAnswerItem(BaseModel):
    question_id: str
    selected_option_id: str


class AssessmentSubmitRequest(BaseModel):
    answers: List[AssessmentAnswerItem]


class SkillGap(BaseModel):
    skill_name: str
    proficiency_score: int  # 0 to 100
    status: str  # proficient, needs_practice, critical_gap
    recommendations: List[str] = Field(default_factory=list)


class AssessmentResultResponse(BaseModel):
    assessment_id: str
    domain: str
    score_percentage: float
    strengths: List[str] = Field(default_factory=list)
    skill_gaps: List[SkillGap] = Field(default_factory=list)
    recommended_roadmap_topics: List[str] = Field(default_factory=list)

