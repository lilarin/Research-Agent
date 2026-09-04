from dataclasses import dataclass
from typing import Generic, TypeVar

from src.enums.nodes import GraphNode
from src.enums.stream import StreamEventType

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class StreamEventData:
    event_ts_ms: int


@dataclass(frozen=True, slots=True)
class WorkflowStartedData(StreamEventData):
    pass


@dataclass(frozen=True, slots=True)
class NodeEventData(StreamEventData):
    node: GraphNode


@dataclass(frozen=True, slots=True)
class NodeStartedData(NodeEventData):
    pass


@dataclass(frozen=True, slots=True)
class NodeFinishedData(NodeEventData):
    duration_ms: int


@dataclass(frozen=True, slots=True)
class MessageData(StreamEventData):
    answer: str


@dataclass(frozen=True, slots=True)
class WorkflowFinishedData(StreamEventData):
    status: str
    first_token_latency_ms: int | None
    generation_duration_ms: int | None


@dataclass(frozen=True, slots=True)
class ErrorData(StreamEventData):
    message: str


@dataclass(frozen=True, slots=True)
class StreamPayload(Generic[T]):
    event: StreamEventType
    data: T
