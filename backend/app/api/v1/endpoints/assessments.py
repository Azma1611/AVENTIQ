from fastapi import APIRouter, HTTPException, status
from app.schemas.assessment import (
    AssessmentStartRequest,
    AssessmentStartResponse,
    AssessmentSubmitRequest,
    AssessmentResultResponse,
)
from app.schemas.common import ApiResponse
from app.services.assessment_service import AssessmentService

router = APIRouter()


@router.post(
    "/start",
    response_model=ApiResponse[AssessmentStartResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Start a diagnostic skill assessment",
)
def start_assessment(request: AssessmentStartRequest):
    assessment = AssessmentService.start_assessment(request)
    return ApiResponse(
        success=True,
        message=f"Assessment started for {request.domain}",
        data=assessment,
    )


@router.post(
    "/{assessment_id}/submit",
    response_model=ApiResponse[AssessmentResultResponse],
    summary="Submit answers and get skill gap analysis",
)
def submit_assessment(assessment_id: str, request: AssessmentSubmitRequest):
    result = AssessmentService.submit_assessment(assessment_id, request)
    return ApiResponse(
        success=True,
        message="Assessment evaluated successfully",
        data=result,
    )


@router.get(
    "/{assessment_id}",
    response_model=ApiResponse[AssessmentResultResponse],
    summary="Get assessment results by ID",
)
def get_assessment_result(assessment_id: str):
    result = AssessmentService.get_result(assessment_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assessment result with id '{assessment_id}' not found",
        )
    return ApiResponse(
        success=True,
        message="Assessment result retrieved successfully",
        data=result,
    )

