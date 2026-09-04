from httpx import HTTPError

from app.logger import log_exception
from src.dataclasses.context import ContextChunk
from src.dataclasses.source import SourceReference
from src.dataclasses.state import ExecutionState
from src.enums.context import ContextSourceType
from src.integrations.search import SearchClient
from src.services.base_context import BaseContextService


class WebContextService(BaseContextService):
    def __init__(self, *, search: SearchClient, max_sources: int) -> None:
        self._search = search
        self._max_sources = max_sources

    async def retrieve(self, state: ExecutionState) -> list[ContextChunk]:
        try:
            response = await self._search.search(
                query=state.search_query,
                max_sources=self._max_sources,
            )
        except HTTPError as error:
            log_exception("Web search context is unavailable", error)
            return []

        return [
            ContextChunk(
                source=SourceReference(
                    type=ContextSourceType.WEB,
                    title=source.title,
                    url=source.url,
                ),
                content=source.content,
            )
            for source in response.sources
        ]
