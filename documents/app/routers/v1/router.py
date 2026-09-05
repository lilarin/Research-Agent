from fastapi import APIRouter

from app.routers.v1.documents import router as documents_router

router = APIRouter(prefix="/v1")
router.include_router(documents_router, prefix="/documents", tags=["Documents"])
