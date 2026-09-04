from ddgs import DDGS
from ddgs.exceptions import DDGSException, TimeoutException

from src.dataclasses.search import SearchResult
from src.exceptions.search import SearchTimeout, SearchUnavailable


class DuckDuckGoSearch:
    def __init__(self, *, timeout: int, region: str) -> None:
        self._timeout = timeout
        self._region = region

    def search(self, query: str, *, max_sources: int) -> list[SearchResult]:
        try:
            with DDGS(timeout=self._timeout) as client:
                results = client.text(
                    query,
                    backend="duckduckgo",
                    region=self._region,
                    max_results=max_sources,
                )
        except TimeoutException as exc:
            raise SearchTimeout("Search provider timed out") from exc
        except DDGSException as exc:
            raise SearchUnavailable("Search provider returned no usable results") from exc

        return [SearchResult(title=result["title"], url=result["href"]) for result in results]
