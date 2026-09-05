from typing import Annotated

from fastapi import Depends

from app.dataclasses.runtime import Runtime
from app.dependencies.runtime import get_runtime
from src.services.search import SearchService


def get_search_service(
        runtime: Annotated[Runtime, Depends(get_runtime)],
) -> SearchService:
    return runtime.search
