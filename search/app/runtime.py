from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import ua_generator
from aiohttp import ClientSession, ClientTimeout, DummyCookieJar, TCPConnector

from app.config import Settings
from app.dataclasses.runtime import Runtime
from src.integrations.duckduckgo import DuckDuckGoSearch
from src.integrations.pages import PageReader
from src.services.search import SearchService


@asynccontextmanager
async def open_runtime(settings: Settings) -> AsyncIterator[Runtime]:
    connector = TCPConnector(limit=settings.page_concurrency)
    async with ClientSession(
            connector=connector,
            timeout=ClientTimeout(total=settings.page_timeout),
            headers={"User-Agent": ua_generator.generate().text},
            cookie_jar=DummyCookieJar(),
    ) as session:
        yield Runtime(
            search=SearchService(
                search=DuckDuckGoSearch(
                    timeout=settings.search_timeout,
                    region=settings.region,
                ),
                pages=PageReader(
                    session=session,
                    max_bytes=settings.page_max_bytes,
                    max_redirects=settings.max_redirects,
                    concurrency=settings.page_concurrency,
                ),
            )
        )
