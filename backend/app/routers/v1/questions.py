from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse

from app.runtime import Runtime, get_runtime
from app.schemas.questions import QuestionRequest
from src.dataclasses.state import ExecutionState

router = APIRouter()


@router.post(
    "",
    response_class=StreamingResponse,
    response_model=None,
    summary="Stream an answer to a question",
    responses={
        status.HTTP_200_OK: {
            "description": "Answer text streamed incrementally",
            "content": {
                "text/plain": {
                    "schema": {"type": "string"},
                    "example": "The answer to your question...",
                },
            },
        },
    },
)
async def answer_question(
        request: QuestionRequest,
        runtime: Annotated[Runtime, Depends(get_runtime)],
) -> StreamingResponse:
    state = ExecutionState(
        conversation_uuid=request.uuid,
        question=request.question,
    )
    return StreamingResponse(
        runtime.stream(state),
    )
