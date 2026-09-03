from dataclasses import dataclass

from src.enums.context import ContextSourceType


@dataclass(slots=True)
class SourceReference:
    type: ContextSourceType
    title: str
    page: int | None = None
    url: str | None = None
