from uuid import UUID

from fastapi import UploadFile
from httpx import AsyncClient

from src.schemas.documents import RetrievalResponse


class DocumentsClient:
    def __init__(self, *, client: AsyncClient) -> None:
        self._client = client

    async def search(
        self,
        *,
        conversation_uuid: UUID,
        query: str,
        max_search: int,
        max_retrieval: int,
    ) -> RetrievalResponse:
        response = await self._client.get(
            "/api/v1/documents/search",
            params={
                "conversation_uuid": str(conversation_uuid),
                "query": query,
                "max_search": max_search,
                "max_retrieval": max_retrieval,
            },
        )
        response.raise_for_status()

        return RetrievalResponse.model_validate(response.json())

    async def upload(self, conversation_uuid: UUID, files: list[UploadFile]) -> None:
        response = await self._client.post(
            "/api/v1/documents",
            data={"conversation_uuid": str(conversation_uuid)},
            files=[
                (
                    "files",
                    (file.filename, file.file, file.content_type),
                )
                for file in files
            ],
        )
        response.raise_for_status()
