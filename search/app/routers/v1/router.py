from fastapi import APIRouter

from app.routers.v1.search import router as search_router

router = APIRouter(prefix="/v1")
router.include_router(search_router, prefix="/search", tags=["Search"])
