from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DocumentInput:
    filename: str
    content_type: str | None
    content: bytes


@dataclass(frozen=True, slots=True)
class DocumentChunk:
    title: str
    content: str
    page: int | None = None
