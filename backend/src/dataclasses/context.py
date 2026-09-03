from dataclasses import dataclass

from src.dataclasses.source import SourceReference


@dataclass(slots=True)
class ContextChunk:
    source: SourceReference
    content: str
