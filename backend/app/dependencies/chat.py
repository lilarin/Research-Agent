from typing import Annotated

from fastapi import Depends

from app.dataclasses.runtime import Runtime
from app.dependencies.runtime import get_runtime
from src.services.chat import ChatService


def get_chat_service(
        runtime: Annotated[Runtime, Depends(get_runtime)],
) -> ChatService:
    return runtime.chat
