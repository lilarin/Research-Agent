from typing import Annotated

from fastapi import Depends

from app.dataclasses.runtime import Runtime
from app.dependencies.runtime import get_runtime
from src.services.documents import DocumentsService


def get_documents_service(
    runtime: Annotated[Runtime, Depends(get_runtime)],
) -> DocumentsService:
    return runtime.documents
