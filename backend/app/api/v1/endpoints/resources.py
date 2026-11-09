from typing import Optional
from fastapi import APIRouter, Query
from app.schemas.resource import ResourceListResponse
from app.schemas.common import ApiResponse
from app.services.resource_service import ResourceService

router = APIRouter()


@router.get(
    "",
    response_model=ApiResponse[ResourceListResponse],
    summary="List curated learning resources with filters",
)
def list_resources(
    skill: Optional[str] = Query(None, description="Filter by skill, e.g. FastAPI, PostgreSQL, Docker"),
    type: Optional[str] = Query(None, description="Filter by resource type: course, documentation, article"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty: beginner, intermediate, advanced"),
    search: Optional[str] = Query(None, description="Search keyword in title or description"),
):
    result = ResourceService.list_resources(
        skill=skill,
        resource_type=type,
        difficulty=difficulty,
        search=search,
    )
    return ApiResponse(
        success=True,
        message=f"Found {result.total} resources",
        data=result,
    )

