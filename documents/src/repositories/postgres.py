from uuid import UUID

from langgraph.store.postgres.aio import AsyncPostgresStore

from src.dataclasses.documents import DocumentChunk


class PostgresDocumentsRepository:
    def __init__(self, *, store: AsyncPostgresStore) -> None:
        self._store = store

    async def exists(
        self,
        conversation_uuid: UUID,
        filename: str | None,
        checksum: str,
    ) -> bool:
        item = await self._store.aget(
            (str(conversation_uuid), "documents"),
            f"{checksum}:{filename}",
        )
        return item is not None

    async def search(
        self,
        conversation_uuid: UUID,
        query: str,
        max_search: int,
    ) -> list[DocumentChunk]:
        results = await self._store.asearch(
            (str(conversation_uuid), "chunks"),
            query=query,
            limit=max_search,
        )
        return [
            DocumentChunk(
                title=item.value["title"],
                content=item.value["text"],
                page=item.value.get("page"),
            )
            for item in results
        ]
