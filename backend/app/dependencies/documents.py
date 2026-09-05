from typing import Annotated

from fastapi import Depends

from app.dataclasses.runtime import Runtime
from app.dependencies.runtime import get_runtime
from src.integrations.documents import DocumentsClient


def get_documents_client(
        runtime: Annotated[Runtime, Depends(get_runtime)],
) -> DocumentsClient:
    return runtime.documents
