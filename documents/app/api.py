from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response

from app.config import get_settings
from app.routers.v1.router import router as router_v1
from app.runtime import open_runtime


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    async with open_runtime(get_settings()) as runtime:
        application.state.runtime = runtime
        yield


app = FastAPI(title="Document Retrieval API", version="1.0", lifespan=lifespan)
app.include_router(router_v1, prefix="/api")


@app.get("/health", tags=["Health"])
async def health() -> Response:
    return Response(status_code=200)
