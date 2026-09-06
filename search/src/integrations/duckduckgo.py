from ddgs import DDGS
from ddgs.exceptions import DDGSException, TimeoutException
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from src.dataclasses.search import SearchResult
from src.exceptions.search import SearchTimeout, SearchUnavailable


class DuckDuckGoSearch:
    def __init__(self, *, timeout: int, region: str) -> None:
        self._timeout = timeout
        self._region = region

    def search(self, query: str, *, max_sources: int) -> list[SearchResult]:
        try:
            results = self._search_with_retry(query, max_sources=max_sources)
        except TimeoutException as exc:
            raise SearchTimeout("Search provider timed out") from exc
        except DDGSException as exc:
            raise SearchUnavailable(
                "Search provider returned no usable results"
            ) from exc

        return [
            SearchResult(title=result["title"], url=result["href"])
            for result in results
        ]

    @retry(
        retry=retry_if_exception_type((DDGSException, TimeoutException)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=2),
        reraise=True,
    )
    def _search_with_retry(
        self, query: str, *, max_sources: int
    ) -> list[dict[str, str]]:
        with DDGS(timeout=self._timeout) as client:
            return client.text(
                query,
                backend="duckduckgo",
                region=self._region,
                max_results=max_sources,
            )
