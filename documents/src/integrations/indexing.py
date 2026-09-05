import asyncio
from io import BytesIO
from uuid import UUID

from docling.chunking import HybridChunker
from docling.datamodel.base_models import DocumentStream
from docling.document_converter import ConversionResult, DocumentConverter
from langgraph.store.base import PutOp
from langgraph.store.postgres.aio import AsyncPostgresStore

from src.dataclasses.documents import DocumentInput


class DocumentIndexingService:
    def __init__(
        self,
        *,
        store: AsyncPostgresStore,
        converter: DocumentConverter,
        chunker: HybridChunker,
        max_file_size: int,
    ) -> None:
        self._store = store
        self._converter = converter
        self._chunker = chunker
        self._max_file_size = max_file_size

    async def process(
        self,
        conversation_uuid: UUID,
        document: DocumentInput,
        checksum: str,
    ) -> None:
        document_name = document.filename
        namespace = (str(conversation_uuid), "chunks", checksum)
        conversion = await self._convert_document(
            document,
            document_name,
        )
        chunks = list(self._chunker.chunk(conversion.document))
        await self._store_chunks(
            namespace,
            chunks,
            document_name,
            checksum,
        )
        await self._store_document(
            conversation_uuid,
            document,
            checksum,
        )

    async def _convert_document(
        self,
        document: DocumentInput,
        document_name: str,
    ) -> ConversionResult:
        return await asyncio.to_thread(
            self._converter.convert,
            DocumentStream(
                name=document_name,
                stream=BytesIO(document.content),
            ),
            max_file_size=self._max_file_size,
        )

    async def _store_chunks(
        self,
        namespace: tuple[str, str, str],
        chunks: list,
        document_name: str,
        checksum: str,
    ) -> None:
        await self._store.abatch(
            PutOp(
                namespace,
                str(index),
                self._chunk_value(chunk, document_name, checksum),
                index=["text"],
            )
            for index, chunk in enumerate(chunks)
        )

    def _chunk_value(
        self,
        chunk,
        document_name: str,
        checksum: str,
    ) -> dict[str, object]:
        return {
            "text": self._chunker.contextualize(chunk),
            "title": self._chunk_title(chunk, document_name),
            "page": self._chunk_page(chunk),
            "checksum": checksum,
        }

    @staticmethod
    def _chunk_title(chunk, document_name: str) -> str:
        return chunk.meta.headings[-1] if chunk.meta.headings else document_name

    @staticmethod
    def _chunk_page(chunk) -> int | None:
        if not chunk.meta.doc_items:
            return None

        item = chunk.meta.doc_items[0]
        return item.prov[0].page_no if item.prov else None

    async def _store_document(
        self,
        conversation_uuid: UUID,
        document: DocumentInput,
        checksum: str,
    ) -> None:
        await self._store.aput(
            (str(conversation_uuid), "documents"),
            f"{checksum}:{document.filename}",
            {
                "filename": document.filename,
                "content_type": document.content_type,
                "checksum": checksum,
            },
            index=False,
        )
