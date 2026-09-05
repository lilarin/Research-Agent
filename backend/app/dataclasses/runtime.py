from dataclasses import dataclass

from src.integrations.documents import DocumentsClient
from src.integrations.search import SearchClient
from src.services.chat import ChatService


@dataclass(frozen=True, slots=True)
class Runtime:
    chat: ChatService
    documents: DocumentsClient
    search: SearchClient
