from pydantic import BaseModel


class DocumentChunk(BaseModel):
    title: str
    content: str
    page: int | None = None


class RetrievalResponse(BaseModel):
    chunks: list[DocumentChunk]
