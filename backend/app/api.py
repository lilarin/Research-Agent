from contextlib import asynccontextmanager

from fastapi import FastAPI, Response, status
from starlette.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers.v1.router import router as router_v1
from app.runtime import open_runtime

settings = get_settings()


@asynccontextmanager
async def lifespan(application: FastAPI):
    async with open_runtime(settings) as runtime:
        application.state.runtime = runtime
        yield


app = FastAPI(title="Research Agent API", version="1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_v1, prefix="/api")


@app.get("/health", tags=["Health"], status_code=status.HTTP_200_OK)
async def health() -> Response:
    return Response(status_code=status.HTTP_200_OK)
