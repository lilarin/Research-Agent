from abc import ABC, abstractmethod

from src.dataclasses.context import ContextChunk
from src.dataclasses.state import ExecutionState


class BaseContextService(ABC):
    @abstractmethod
    async def retrieve(self, state: ExecutionState) -> list[ContextChunk]:
        ...
