from fastapi import APIRouter

from app.routers.v1.documents import router as documents_router
from app.routers.v1.questions import router as questions_router

router = APIRouter(prefix="/v1")

router.include_router(questions_router, prefix="/questions", tags=["Questions"])
router.include_router(documents_router, prefix="/documents", tags=["Documents"])
