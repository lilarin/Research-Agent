import asyncio
import json
from collections.abc import AsyncIterator
from dataclasses import asdict
from time import perf_counter
from typing import Any

from app.runtime import Runtime
from src.dataclasses.state import ExecutionState
from src.dataclasses.stream import StreamPayload
from src.streaming.processor import StreamProcessor


def serialize_sse_event(payload: StreamPayload[Any]) -> dict[str, str]:
    return {
        "event": payload.event.value,
        "data": json.dumps(asdict(payload.data), ensure_ascii=False),
    }


async def stream_sse(
        runtime: Runtime,
        state: ExecutionState,
) -> AsyncIterator[dict[str, str]]:
    processor = StreamProcessor(perf_counter())
    yield serialize_sse_event(processor.workflow_started())
    try:
        async for event in runtime.stream_events(state):
            if payload := processor.handle(event):
                yield serialize_sse_event(payload)
        yield serialize_sse_event(processor.workflow_finished())
    except asyncio.CancelledError:
        raise
    except Exception:
        yield serialize_sse_event(processor.error("Service unavailable"))
