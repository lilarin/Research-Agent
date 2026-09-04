from pydantic import BaseModel


class SearchSource(BaseModel):
    title: str
    url: str
    content: str


class SearchResponse(BaseModel):
    sources: list[SearchSource]
