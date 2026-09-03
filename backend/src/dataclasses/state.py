from dataclasses import dataclass, field
from typing import Annotated
from uuid import UUID

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from src.dataclasses.context import ContextChunk
from src.schemas.intent import IntentDecision


@dataclass(slots=True)
class ExecutionState:
    conversation_uuid: UUID
    question: str = ""
    intent: IntentDecision | None = None
    context: list[ContextChunk] = field(default_factory=list)
    history_messages: Annotated[list[BaseMessage], add_messages] = field(
        default_factory=list,
    )
    answer: str = ""
