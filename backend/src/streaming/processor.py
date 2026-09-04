from time import perf_counter, time_ns
from typing import Any, TypeVar, cast

from langchain_core.messages import BaseMessage

from src.dataclasses.stream import (
    ErrorData,
    MessageData,
    NodeFinishedData,
    NodeStartedData,
    StreamPayload,
    WorkflowFinishedData,
    WorkflowStartedData,
)
from src.enums.nodes import GraphNode
from src.enums.stream import StreamEventType

T = TypeVar("T")


class StreamProcessor:
    def __init__(self, request_started_at: float) -> None:
        self._request_started_at = request_started_at
        self._started_nodes: dict[str, tuple[GraphNode, float]] = {}
        self._first_token_at: float | None = None
        self._last_token_at: float | None = None

    def workflow_started(self) -> StreamPayload:
        return self._payload(
            StreamEventType.WORKFLOW_STARTED,
            WorkflowStartedData(event_ts_ms=self._now_ms()),
        )

    def handle(self, event: dict[str, object]) -> StreamPayload | None:
        if event["type"] == "tasks":
            return self._handle_task(cast(dict[str, Any], event["data"]))
        if event["type"] == "messages":
            return self._handle_message(
                cast(tuple[BaseMessage, dict[str, Any]], event["data"])
            )
        return None

    def workflow_finished(self) -> StreamPayload:
        return self._payload(
            StreamEventType.WORKFLOW_FINISHED,
            WorkflowFinishedData(
                status="succeeded",
                event_ts_ms=self._now_ms(),
                first_token_latency_ms=self._first_token_latency_ms,
                generation_duration_ms=self._generation_duration_ms,
            ),
        )

    def error(self, message: str) -> StreamPayload:
        return self._payload(
            StreamEventType.ERROR,
            ErrorData(event_ts_ms=self._now_ms(), message=message),
        )

    def _handle_task(self, data: dict[str, Any]) -> StreamPayload:
        task_id = str(data["id"])
        node = GraphNode(data["name"])
        now = perf_counter()
        if "input" in data:
            self._started_nodes[task_id] = node, now
            return self._payload(
                StreamEventType.NODE_STARTED,
                NodeStartedData(event_ts_ms=self._now_ms(), node=node),
            )

        started = self._started_nodes.pop(task_id)[1]
        return self._payload(
            StreamEventType.NODE_FINISHED,
            NodeFinishedData(
                event_ts_ms=self._now_ms(),
                node=node,
                duration_ms=round((now - started) * 1000),
            ),
        )

    def _handle_message(
            self,
            data: tuple[BaseMessage, dict[str, Any]],
    ) -> StreamPayload | None:
        message, metadata = data
        node = GraphNode(metadata["langgraph_node"])
        if not node.is_streamable or not message.text:
            return None

        now = perf_counter()
        self._first_token_at = self._first_token_at or now
        self._last_token_at = now
        return self._payload(
            StreamEventType.MESSAGE,
            MessageData(event_ts_ms=self._now_ms(), answer=message.text),
        )

    @property
    def _first_token_latency_ms(self) -> int | None:
        if self._first_token_at is None:
            return None
        return round((self._first_token_at - self._request_started_at) * 1000)

    @property
    def _generation_duration_ms(self) -> int | None:
        if self._first_token_at is None or self._last_token_at is None:
            return None
        return round((self._last_token_at - self._first_token_at) * 1000)

    @staticmethod
    def _now_ms() -> int:
        return time_ns() // 1_000_000

    @staticmethod
    def _payload(event: StreamEventType, data: T) -> StreamPayload[T]:
        return StreamPayload(event=event, data=data)
