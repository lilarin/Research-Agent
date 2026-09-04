from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        extra="ignore",
    )

    host: str = Field(default="0.0.0.0", alias="SEARCH_HOST")
    port: int = Field(default=8002, alias="SEARCH_PORT")
    debug: bool = Field(default=False, alias="DEBUG")
    region: str = Field(default="de-de", alias="SEARCH_REGION")
    search_timeout: int = Field(default=10, alias="SEARCH_TIMEOUT")
    page_timeout: float = Field(default=10, alias="SEARCH_PAGE_TIMEOUT")
    page_max_bytes: int = Field(default=10_000_000, alias="SEARCH_PAGE_MAX_BYTES")
    page_concurrency: int = Field(default=5, alias="SEARCH_PAGE_CONCURRENCY")
    max_redirects: int = Field(default=3, alias="SEARCH_MAX_REDIRECTS")


@lru_cache
def get_settings() -> Settings:
    return Settings()
