from httpx import AsyncClient

from src.schemas.search import SearchResponse


class SearchClient:
    def __init__(self, *, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")

    async def search(self, *, query: str, max_sources: int) -> SearchResponse:
        async with AsyncClient(base_url=self._base_url) as client:
            response = await client.post(
                "/api/v1/search",
                json={"query": query, "max_sources": max_sources},
            )
            response.raise_for_status()

        return SearchResponse.model_validate(response.json())
