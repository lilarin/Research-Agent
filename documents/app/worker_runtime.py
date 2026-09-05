from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from docling.chunking import HybridChunker
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter

from app.config import Settings
from app.resources import open_store
from src.integrations.indexing import DocumentIndexingService


@dataclass(frozen=True, slots=True)
class WorkerRuntime:
    indexing: DocumentIndexingService


@asynccontextmanager
async def open_worker_runtime(settings: Settings) -> AsyncIterator[WorkerRuntime]:
    async with open_store(settings) as store:
        yield WorkerRuntime(
            indexing=DocumentIndexingService(
                store=store,
                converter=DocumentConverter(
                    allowed_formats=[InputFormat(value) for value in settings.formats]
                ),
                chunker=HybridChunker(),
                max_file_size=settings.max_upload_bytes,
            )
        )
