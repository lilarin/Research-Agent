from typing import Annotated

from fastapi import APIRouter, Depends, status
from sse_starlette.sse import EventSourceResponse

from app.runtime import Runtime, get_runtime
from app.schemas.questions import QuestionRequest
from src.dataclasses.state import ExecutionState
from src.streaming.pipeline import stream_sse

router = APIRouter()


@router.post(
    "",
    response_class=EventSourceResponse,
    response_model=None,
    summary="Stream an answer to a question",
    responses={
        status.HTTP_200_OK: {
            "description": "Answer text streamed incrementally",
            "content": {
                "text/event-stream": {
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
) -> EventSourceResponse:
    state = ExecutionState(
        conversation_uuid=request.uuid,
        question=request.question,
    )
    return EventSourceResponse(stream_sse(runtime, state))
