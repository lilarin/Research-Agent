from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class RetrievalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    conversation_uuid: UUID
    query: str = Field(min_length=1)
    max_search: int = Field(gt=0)
    max_retrieval: int = Field(gt=0)

    @model_validator(mode="after")
    def validate_limits(self) -> Self:
        if self.max_retrieval > self.max_search:
            raise ValueError("max_retrieval must not exceed max_search")
        return self


class DocumentChunkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    content: str
    page: int | None = None


class RetrievalResponse(BaseModel):
    chunks: list[DocumentChunkResponse]
