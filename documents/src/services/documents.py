from hashlib import sha256
from uuid import UUID

from src.dataclasses.documents import DocumentChunk, DocumentInput
from src.integrations.arq import ArqDocumentsQueue
from src.repositories.postgres import PostgresDocumentsRepository


class DocumentsService:
    def __init__(
        self,
        *,
        queue: ArqDocumentsQueue,
        repository: PostgresDocumentsRepository,
    ) -> None:
        self._queue = queue
        self._repository = repository

    async def upload(
        self,
        conversation_uuid: UUID,
        documents: list[DocumentInput],
    ) -> None:
        for document in documents:
            checksum = sha256(document.content).hexdigest()
            if await self._repository.exists(
                conversation_uuid,
                document.filename,
                checksum,
            ):
                continue
            await self._queue.enqueue(conversation_uuid, document, checksum)

    async def search(
        self,
        conversation_uuid: UUID,
        query: str,
        max_search: int,
        max_retrieval: int,
    ) -> list[DocumentChunk]:
        chunks = await self._repository.search(
            conversation_uuid,
            query,
            max_search,
        )
        return chunks[:max_retrieval]
