import uvicorn

from app.config import get_settings


def run_api() -> None:
    settings = get_settings()
    uvicorn.run(
        "app.api:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info",
    )


if __name__ == "__main__":
    run_api()
