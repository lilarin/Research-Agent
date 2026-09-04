from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.search import get_search_service
from app.schemas.search import SearchRequest, SearchResponse, SourceResponse
from logger import log_exception
from src.exceptions.search import ContentUnavailable, SearchTimeout, SearchUnavailable
from src.services.search import SearchService

router = APIRouter()


@router.post(
    "",
    response_model=SearchResponse,
    summary="Search the web and extract page text",
)
async def search_web(
        request: SearchRequest,
        service: Annotated[SearchService, Depends(get_search_service)],
) -> SearchResponse:
    try:
        sources = await service.search(
            request.query,
            max_sources=request.max_sources
        )
    except (SearchTimeout, SearchUnavailable, ContentUnavailable) as exc:
        log_exception("Web search failed", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to retrieve web search results",
        ) from exc
    return SearchResponse(
        sources=[
            SourceResponse.model_validate(source)
            for source in sources
        ]
    )
