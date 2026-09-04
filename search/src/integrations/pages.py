from asyncio import Semaphore, to_thread

from aiohttp import ClientError, ClientSession
from trafilatura import extract

from logger import logger
from src.dataclasses.search import SearchResult, WebSource


class PageReader:
    def __init__(
            self, *, session: ClientSession, max_bytes: int, max_redirects: int, concurrency: int,
    ) -> None:
        self._session = session
        self._max_bytes = max_bytes
        self._max_redirects = max_redirects
        self._semaphore = Semaphore(concurrency)

    async def read(self, result: SearchResult) -> WebSource | None:
        async with self._semaphore:
            try:
                async with self._session.get(
                        result.url, max_redirects=self._max_redirects
                ) as response:
                    response.raise_for_status()

                    if response.content_type not in {"text/html", "application/xhtml+xml", "text/plain"}:
                        logger.info("Page skipped: %s (unsupported content type)", result.url)
                        return None
                    if response.content_length is not None and response.content_length > self._max_bytes:
                        logger.info("Page skipped: %s (download size limit exceeded)", result.url)
                        return None

                    body = bytearray()
                    async for chunk in response.content.iter_any():
                        body.extend(chunk)
                        if len(body) > self._max_bytes:
                            logger.info("Page skipped: %s (download size limit exceeded)", result.url)
                            return None

                    url = str(response.url)
                    if response.content_type == "text/plain":
                        content = body.decode(response.charset or "utf-8", errors="replace").strip()
                    else:
                        content = await to_thread(
                            extract,
                            bytes(body),
                            url=url,
                            include_comments=False,
                            include_tables=False,
                            include_links=False,
                            favor_precision=True,
                        )
            except (ClientError, OSError, TimeoutError) as exc:
                logger.info("Page skipped: %s (%s)", result.url, exc)
                return None

            if not content:
                logger.info("Page skipped: %s (no readable text)", result.url)
                return None

            return WebSource(title=result.title, url=url, content=content)
