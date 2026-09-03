from src.dataclasses.context import ContextChunk
from src.dataclasses.state import ExecutionState
from src.services.base_context import BaseContextService


class WebContextService(BaseContextService):
    async def retrieve(self, state: ExecutionState) -> list[ContextChunk]:
        return []
