from fastapi import FastAPI, Response

from app.routers.v1.router import router as router_v1

app = FastAPI(title="Web Search API", version="1.0")
app.include_router(router_v1, prefix="/api")


@app.get("/health", tags=["Health"])
async def health() -> Response:
    return Response(status_code=200)
