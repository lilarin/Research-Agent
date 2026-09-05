from uuid import UUID

from arq import ArqRedis

from src.dataclasses.documents import DocumentInput


class ArqDocumentsQueue:
    def __init__(self, *, redis: ArqRedis, queue_name: str) -> None:
        self._redis = redis
        self._queue_name = queue_name

    async def enqueue(
        self,
        conversation_uuid: UUID,
        document: DocumentInput,
        checksum: str,
    ) -> None:
        await self._redis.enqueue_job(
            "index_document",
            conversation_uuid,
            document,
            checksum,
            _job_id=f"{conversation_uuid}:{checksum}:{document.filename}",
            _queue_name=self._queue_name,
        )
