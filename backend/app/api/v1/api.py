from fastapi import APIRouter
from app.api.v1.endpoints import roadmaps, assessments, mentor, resources

api_router = APIRouter()

api_router.include_router(
    roadmaps.router,
    prefix="/roadmaps",
    tags=["Career Roadmaps"],
)

api_router.include_router(
    assessments.router,
    prefix="/assessments",
    tags=["Skill Assessments & Gap Analysis"],
)

api_router.include_router(
    mentor.router,
    prefix="/mentor",
    tags=["AI Career Mentor"],
)

api_router.include_router(
    resources.router,
    prefix="/resources",
    tags=["Curated Learning Resources"],
)

