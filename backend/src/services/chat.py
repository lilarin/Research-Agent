from collections.abc import AsyncIterator
from contextlib import aclosing
from typing import Any, Literal, cast
from uuid import UUID

from langchain_core.messages import BaseMessage
from langgraph.graph.state import CompiledStateGraph

from app.logger import log_exception
from src.dataclasses.state import ExecutionState
from src.enums.nodes import GraphNode
from src.repositories.chat import ChatHistoryRepository


class ChatService:
    def __init__(
            self,
            *,
            graph: CompiledStateGraph,
            history: ChatHistoryRepository,
    ) -> None:
        self._graph = graph
        self._history = history

    async def run(self, state: ExecutionState) -> dict[str, object]:
        return await self._graph.ainvoke(state)

    async def stream_answer(
            self,
            state: ExecutionState,
    ) -> AsyncIterator[dict[str, object]]:
        state.history_messages = await self._history.get(state.conversation_uuid)
        answer_parts: list[str] = []
        stream_mode: tuple[Literal["tasks", "messages"], ...] = (
            "tasks",
            "messages",
        )
        stream = self._graph.astream(
            cast(Any, state),
            stream_mode=stream_mode,
            version="v2",
        )
        async with aclosing(stream):
            async for event in stream:
                if answer := self._answer_part(event):
                    answer_parts.append(answer)
                yield event

        answer = "".join(answer_parts)
        if answer:
            await self._save_chat_history(
                conversation_uuid=state.conversation_uuid,
                question=state.question,
                answer=answer,
            )

    async def _save_chat_history(
            self,
            *,
            conversation_uuid: UUID,
            question: str,
            answer: str,
    ) -> None:
        try:
            await self._history.append(
                conversation_uuid=conversation_uuid,
                question=question,
                answer=answer,
            )
        except Exception as error:
            log_exception(
                f"Failed to save chat history for conversation {conversation_uuid}",
                error,
            )

    @staticmethod
    def _answer_part(event: dict[str, object]) -> str:
        if event["type"] != "messages":
            return ""

        message, metadata = cast(
            tuple[BaseMessage, dict[str, Any]],
            event["data"],
        )
        node = GraphNode(metadata["langgraph_node"])
        if not node.is_streamable:
            return ""
        return message.text
