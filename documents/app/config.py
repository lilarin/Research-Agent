from functools import lru_cache
from pathlib import Path

from arq.connections import RedisSettings
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        extra="ignore",
    )

    host: str = Field("0.0.0.0", alias="DOCUMENTS_HOST")
    port: int = Field(8001, alias="DOCUMENTS_PORT")
    debug: bool = Field(False, alias="DEBUG")
    postgres_host: str = Field("postgres", alias="POSTGRES_HOST")
    postgres_port: int = Field(5432, alias="POSTGRES_PORT")
    postgres_db: str = Field("research", alias="POSTGRES_DB")
    postgres_user: str = Field("postgres", alias="POSTGRES_USER")
    postgres_password: str = Field("postgres", alias="POSTGRES_PASSWORD")
    postgres_pool_min_size: int = Field(1, gt=0, alias="POSTGRES_POOL_MIN_SIZE")
    postgres_pool_max_size: int = Field(4, gt=0, alias="POSTGRES_POOL_MAX_SIZE")
    redis_host: str = Field("redis", alias="REDIS_HOST")
    redis_port: int = Field(6379, alias="REDIS_PORT")
    redis_db: int = Field(0, alias="REDIS_DB")
    queue_name: str = Field("documents:index", alias="DOCUMENTS_QUEUE")
    max_upload_bytes: int = Field(25_000_000, gt=0, alias="DOCUMENTS_MAX_UPLOAD_BYTES")
    max_files: int = Field(10, gt=0, alias="DOCUMENTS_MAX_FILES")
    formats: list[str] = Field(
        [
            "pdf",
            "docx",
            "pptx",
            "xlsx",
            "html",
            "md",
            "csv",
            "image",
        ],
        alias="DOCUMENTS_FORMATS",
    )
    job_timeout: int = Field(1800, gt=0, alias="DOCUMENTS_JOB_TIMEOUT")
    max_jobs: int = Field(1, gt=0, alias="DOCUMENTS_MAX_JOBS")
    max_tries: int = Field(3, gt=0, alias="DOCUMENTS_MAX_TRIES")
    model_base_url: str = Field("http://ollama:11434", alias="MODEL_BASE_URL")
    embedding_timeout: float = Field(120, gt=0, alias="EMBEDDING_TIMEOUT")
    embedding_model: str = Field(..., alias="EMBEDDING_MODEL")
    embedding_dimensions: int = Field(..., gt=0, alias="EMBEDDING_DIMENSIONS")

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    def redis_settings(self) -> RedisSettings:
        return RedisSettings(
            host=self.redis_host, port=self.redis_port, database=self.redis_db
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
