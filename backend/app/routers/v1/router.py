from fastapi import APIRouter

from app.routers.v1.questions import router as questions_router

router = APIRouter(prefix="/v1")

router.include_router(questions_router, prefix="/questions", tags=["Questions"])
