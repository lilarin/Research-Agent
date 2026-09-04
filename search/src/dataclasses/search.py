from dataclasses import dataclass


@dataclass(slots=True)
class SearchResult:
    title: str
    url: str


@dataclass(slots=True)
class WebSource:
    title: str
    url: str
    content: str
