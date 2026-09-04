from pydantic import BaseModel, ConfigDict, Field


class SearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    query: str = Field(min_length=1)
    max_sources: int = Field(
        default=5, ge=1, le=20
    )


class SourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    url: str
    content: str


class SearchResponse(BaseModel):
    sources: list[SourceResponse]
