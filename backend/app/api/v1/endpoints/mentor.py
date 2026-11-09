from fastapi import APIRouter
from app.schemas.mentor import MentorChatRequest, MentorChatResponse
from app.schemas.common import ApiResponse
from app.services.mentor_service import MentorService

router = APIRouter()


@router.post(
    "/chat",
    response_model=ApiResponse[MentorChatResponse],
    summary="Chat with the AVENTIQ AI Career Mentor",
)
def chat_with_mentor(request: MentorChatRequest):
    mentor_response = MentorService.chat(request)
    return ApiResponse(
        success=True,
        message="Mentor advice generated",
        data=mentor_response,
    )

