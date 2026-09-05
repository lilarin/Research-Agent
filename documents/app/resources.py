from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from arq import create_pool
from arq.connections import ArqRedis
from langchain_ollama import OllamaEmbeddings
from langgraph.store.postgres import PoolConfig
from langgraph.store.postgres.aio import AsyncPostgresStore

from app.config import Settings


@asynccontextmanager
async def open_store(settings: Settings) -> AsyncIterator[AsyncPostgresStore]:
    async with AsyncPostgresStore.from_conn_string(
            settings.postgres_dsn,
            pool_config=PoolConfig(
                min_size=settings.postgres_pool_min_size,
                max_size=settings.postgres_pool_max_size,
            ),
            index={
                "dims": settings.embedding_dimensions,
                "embed": OllamaEmbeddings(
                    model=settings.embedding_model,
                    base_url=settings.model_base_url,
                    async_client_kwargs={"timeout": settings.embedding_timeout},
                ),
                "fields": ["text"],
            },
    ) as store:
        yield store


@asynccontextmanager
async def open_redis(settings: Settings) -> AsyncIterator[ArqRedis]:
    redis = await create_pool(settings.redis_settings())
    try:
        yield redis
    finally:
        await redis.close()
