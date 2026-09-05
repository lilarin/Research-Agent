from typing import Annotated
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Response,
    UploadFile,
    status,
)
from httpx import HTTPStatusError, RequestError

from app.dependencies.documents import get_documents_client
from app.config import Settings, get_settings
from app.logger import log_exception
from src.integrations.documents import DocumentsClient

router = APIRouter()


@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def upload_documents(
        conversation_uuid: Annotated[UUID, Form()],
        files: Annotated[list[UploadFile], File()],
        settings: Annotated[Settings, Depends(get_settings)],
        client: Annotated[DocumentsClient, Depends(get_documents_client)],
) -> Response:
    for file in files:
        content = await file.read(settings.documents_max_upload_bytes + 1)
        if len(content) > settings.documents_max_upload_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=(
                    "Maximum file size is "
                    f"{settings.documents_max_upload_bytes} bytes"
                ),
            )
        await file.seek(0)

    try:
        await client.upload(conversation_uuid, files)
        return Response(status_code=status.HTTP_202_ACCEPTED)
    except HTTPStatusError as error:
        if error.response.status_code in {
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        }:
            raise HTTPException(
                status_code=error.response.status_code,
                detail=error.response.json()["detail"],
            ) from error
        log_exception("Document service unavailable", error)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Document service unavailable",
        ) from error
    except RequestError as error:
        log_exception("Document service unavailable", error)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Document service unavailable",
        ) from error
