from httpx import HTTPError

from app.logger import log_exception
from src.dataclasses.context import ContextChunk
from src.dataclasses.source import SourceReference
from src.dataclasses.state import ExecutionState
from src.enums.context import ContextSourceType
from src.integrations.documents import DocumentsClient
from src.services.base_context import BaseContextService


class DocumentsContextService(BaseContextService):
    def __init__(
        self,
        *,
        documents: DocumentsClient,
        max_search: int,
        max_retrieval: int,
    ):
        self._documents = documents
        self._max_search = max_search
        self._max_retrieval = max_retrieval

    async def retrieve(self, state: ExecutionState) -> list[ContextChunk]:
        try:
            response = await self._documents.search(
                conversation_uuid=state.conversation_uuid,
                query=state.search_query,
                max_search=self._max_search,
                max_retrieval=self._max_retrieval,
            )
        except HTTPError as error:
            log_exception("Document context is unavailable", error)
            return []

        return [
            ContextChunk(
                source=SourceReference(
                    type=ContextSourceType.DOCUMENT,
                    title=chunk.title,
                    page=chunk.page,
                ),
                content=chunk.content,
            )
            for chunk in response.chunks
        ]
