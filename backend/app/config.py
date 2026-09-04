from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    host: str = Field(default="0.0.0.0", alias="BACKEND_HOST")
    port: int = Field(default=8000, alias="BACKEND_PORT")
    debug: bool = Field(default=False, alias="DEBUG")
    cors_origins: list[str] = Field(
        default=["http://localhost:5173"],
        alias="CORS_ORIGINS",
    )

    postgres_host: str = Field(default="postgres", alias="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, alias="POSTGRES_PORT")
    postgres_db: str = Field(default="research", alias="POSTGRES_DB")
    postgres_user: str = Field(default="postgres", alias="POSTGRES_USER")
    postgres_password: str = Field(
        default="postgres",
        alias="POSTGRES_PASSWORD",
    )

    redis_host: str = Field(default="redis", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_db: int = Field(default=0, alias="REDIS_DB")

    model_base_url: str = Field(
        default="http://ollama:11434",
        alias="MODEL_BASE_URL",
    )
    llm_model: str = Field(default="qwen3:4b", alias="LLM_MODEL")
    llm_max_retries: int = Field(default=2, alias="LLM_MAX_RETRIES")
    llm_retry_after: int = Field(default=1, alias="LLM_RETRY_AFTER")
    llm_timeout: float = Field(default=120.0, alias="LLM_TIMEOUT")
    llm_answer_think: str = Field(default="low", alias="LLM_ANSWER_THINK")
    embedding_model: str = Field(
        default="embeddinggemma:300m-qat-q4_0",
        alias="EMBEDDING_MODEL",
    )
    reranker_model: str = Field(
        default="dengcao/Qwen3-Reranker-0.6B:Q8_0",
        alias="RERANKER_MODEL",
    )

    chat_history_messages_limit: int = 10


@lru_cache
def get_settings() -> Settings:
    return Settings()
