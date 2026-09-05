from dataclasses import dataclass

from src.services.documents import DocumentsService


@dataclass(frozen=True, slots=True)
class Runtime:
    documents: DocumentsService
