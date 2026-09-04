from collections.abc import AsyncIterator
from typing import Annotated

import ua_generator
from aiohttp import ClientSession, ClientTimeout, DummyCookieJar, TCPConnector
from fastapi import Depends

from app.config import Settings, get_settings
from src.integrations.duckduckgo import DuckDuckGoSearch
from src.integrations.pages import PageReader
from src.services.search import SearchService


async def get_search_service(
        settings: Annotated[Settings, Depends(get_settings)],
) -> AsyncIterator[SearchService]:
    connector = TCPConnector(limit=settings.page_concurrency)
    async with ClientSession(
            connector=connector,
            timeout=ClientTimeout(total=settings.page_timeout),
            headers={"User-Agent": ua_generator.generate().text},
            cookie_jar=DummyCookieJar(),
    ) as session:
        yield SearchService(
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
