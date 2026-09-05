from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager

from app.config import Settings
from app.dataclasses.runtime import Runtime
from app.resources import open_redis, open_store
from src.integrations.arq import ArqDocumentsQueue
from src.repositories.postgres import PostgresDocumentsRepository
from src.services.documents import DocumentsService


@asynccontextmanager
async def open_runtime(settings: Settings) -> AsyncIterator[Runtime]:
    async with AsyncExitStack() as stack:
        store = await stack.enter_async_context(open_store(settings))
        redis = await stack.enter_async_context(open_redis(settings))
        repository = PostgresDocumentsRepository(store=store)
        queue = ArqDocumentsQueue(redis=redis, queue_name=settings.queue_name)
        yield Runtime(
            documents=DocumentsService(
                queue=queue,
                repository=repository
            )
        )
