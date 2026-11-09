from fastapi import APIRouter, HTTPException, status
from app.schemas.roadmap import (
    RoadmapCreateRequest,
    RoadmapResponse,
    MilestoneUpdateRequest,
)
from app.schemas.common import ApiResponse
from app.services.roadmap_service import RoadmapService

router = APIRouter()


@router.post(
    "/generate",
    response_model=ApiResponse[RoadmapResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Generate a personalized career roadmap",
)
def generate_roadmap(request: RoadmapCreateRequest):
    roadmap = RoadmapService.generate_roadmap(request)
    return ApiResponse(
        success=True,
        message=f"Personalized roadmap generated for {request.target_role}",
        data=roadmap,
    )


@router.get(
    "/{roadmap_id}",
    response_model=ApiResponse[RoadmapResponse],
    summary="Get roadmap by ID",
)
def get_roadmap(roadmap_id: str):
    roadmap = RoadmapService.get_roadmap(roadmap_id)
    if not roadmap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Roadmap with id '{roadmap_id}' not found",
        )
    return ApiResponse(
        success=True,
        message="Roadmap retrieved successfully",
        data=roadmap,
    )


@router.patch(
    "/{roadmap_id}/milestones/{milestone_id}",
    response_model=ApiResponse[RoadmapResponse],
    summary="Update milestone completion status",
)
def update_milestone_status(
    roadmap_id: str, milestone_id: str, request: MilestoneUpdateRequest
):
    updated = RoadmapService.update_milestone_status(
        roadmap_id=roadmap_id,
        milestone_id=milestone_id,
        is_completed=request.is_completed,
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Roadmap or milestone not found",
        )
    return ApiResponse(
        success=True,
        message=f"Milestone status updated to {'completed' if request.is_completed else 'pending'}",
        data=updated,
    )

