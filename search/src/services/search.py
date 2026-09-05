import asyncio

from src.dataclasses.search import WebSource
from src.exceptions.search import ContentUnavailable
from src.integrations.duckduckgo import DuckDuckGoSearch
from src.integrations.pages import PageReader


class SearchService:
    def __init__(self, *, search: DuckDuckGoSearch, pages: PageReader) -> None:
        self._search = search
        self._pages = pages

    async def search(self, query: str, *, max_sources: int) -> list[WebSource]:
        results = await asyncio.to_thread(
            self._search.search, query, max_sources=max_sources
        )
        async with asyncio.TaskGroup() as group:
            tasks = [group.create_task(self._pages.read(result)) for result in results]

        sources = [source for task in tasks if (source := task.result()) is not None]
        if not sources:
            raise ContentUnavailable("None of the search results could be read")
        return sources[:max_sources]
