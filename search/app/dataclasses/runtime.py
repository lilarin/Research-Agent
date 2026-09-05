from dataclasses import dataclass

from src.services.search import SearchService


@dataclass(frozen=True, slots=True)
class Runtime:
    search: SearchService
