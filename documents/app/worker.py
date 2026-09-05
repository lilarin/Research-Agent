from collections.abc import Callable
from typing import Any, ClassVar
from uuid import UUID

from arq.connections import RedisSettings

from app.config import get_settings
from app.logger import log_exception

from app.worker_runtime import WorkerRuntime, open_worker_runtime
from src.dataclasses.documents import DocumentInput


async def index_document(
    ctx: dict[str, Any],
    conversation_uuid: UUID,
    document: DocumentInput,
    checksum: str,
) -> None:
    runtime: WorkerRuntime = ctx["runtime"]
    try:
        await runtime.indexing.process(conversation_uuid, document, checksum)
    except Exception as error:
        log_exception(
            "Document indexing failed: "
            f"conversation={conversation_uuid} "
            f"filename={document.filename} "
            f"checksum={checksum} "
            f"job_try={ctx.get('job_try', 'unknown')}",
            error,
        )
        raise


async def startup(ctx: dict[str, Any]) -> None:
    context = open_worker_runtime(get_settings())
    ctx["runtime_context"] = context
    ctx["runtime"] = await context.__aenter__()


async def shutdown(ctx: dict[str, Any]) -> None:
    await ctx["runtime_context"].__aexit__(None, None, None)


class WorkerSettings:
    functions: ClassVar[list[Callable[..., Any]]] = [index_document]
    redis_settings: ClassVar[RedisSettings] = get_settings().redis_settings()
    queue_name: ClassVar[str] = get_settings().queue_name
    max_jobs: ClassVar[int] = get_settings().max_jobs
    job_timeout: ClassVar[int] = get_settings().job_timeout
    max_tries: ClassVar[int] = get_settings().max_tries
    on_startup = startup
    on_shutdown = shutdown
