from typing import Annotated
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    Response,
    UploadFile,
    status,
)
from psycopg import Error as PsycopgError
from redis.exceptions import RedisError

from app.config import Settings, get_settings
from app.dependencies.documents import get_documents_service
from app.logger import log_exception
from app.schemas.documents import (
    DocumentChunkResponse,
    RetrievalRequest,
    RetrievalResponse,
)
from src.dataclasses.documents import DocumentInput
from src.services.documents import DocumentsService

router = APIRouter()


@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def upload_documents(
    conversation_uuid: Annotated[UUID, Form()],
    files: Annotated[list[UploadFile], File()],
    settings: Annotated[Settings, Depends(get_settings)],
    service: Annotated[DocumentsService, Depends(get_documents_service)],
) -> Response:
    if len(files) > settings.max_files:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Maximum number of files is {settings.max_files}",
        )

    documents: list[DocumentInput] = []
    for file in files:
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Filename is required",
            )
        content = await file.read(settings.max_upload_bytes + 1)
        if len(content) > settings.max_upload_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Maximum file size is {settings.max_upload_bytes} bytes",
            )
        documents.append(
            DocumentInput(
                filename=file.filename,
                content_type=file.content_type,
                content=content,
            )
        )

    try:
        await service.upload(
            conversation_uuid,
            documents,
        )
    except (PsycopgError, RedisError) as error:
        log_exception("Document infrastructure is unavailable", error)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Document service is temporarily unavailable",
        ) from error
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.get("/search", response_model=RetrievalResponse)
async def search_documents(
    request: Annotated[RetrievalRequest, Query()],
    service: Annotated[DocumentsService, Depends(get_documents_service)],
) -> RetrievalResponse:
    try:
        chunks = await service.search(
            request.conversation_uuid,
            request.query,
            request.max_search,
            request.max_retrieval,
        )
    except PsycopgError as error:
        log_exception("Document infrastructure is unavailable", error)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Document service is temporarily unavailable",
        ) from error

    return RetrievalResponse(
        chunks=[DocumentChunkResponse.model_validate(chunk) for chunk in chunks]
    )
