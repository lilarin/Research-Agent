from httpx import AsyncClient

from src.schemas.search import SearchResponse


class SearchClient:
    def __init__(self, *, client: AsyncClient) -> None:
        self._client = client

    async def search(self, *, query: str, max_sources: int) -> SearchResponse:
        response = await self._client.get(
            "/api/v1/search",
            params={
                "query": query,
                "max_sources": max_sources,
            },
        )
        response.raise_for_status()

        return SearchResponse.model_validate(response.json())
