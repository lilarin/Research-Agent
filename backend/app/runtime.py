from collections.abc import AsyncIterator
from contextlib import aclosing
from functools import lru_cache
from typing import Any, Literal, cast

from langchain_litellm import ChatLiteLLMRouter
from langgraph.graph.state import CompiledStateGraph
from litellm import Router

from app.config import Settings, get_settings
from src.dataclasses.state import ExecutionState
from src.graph.graph import build_research_graph
from src.graph.nodes import ResearchGraphNodes
from src.services.documents_context import DocumentsContextService
from src.services.web_context import WebContextService
from src.steps.answer import AnswerStep
from src.steps.clarification import ClarificationStep
from src.steps.mode_selection import ModeSelectionStep
from src.steps.out_of_scope import OutOfScopeStep
from src.steps.routing import RoutingStep


class Runtime:
    def __init__(
            self,
            *,
            graph: CompiledStateGraph,
    ) -> None:
        self._graph = graph

    async def run(self, state: ExecutionState) -> dict[str, object]:
        return await self._graph.ainvoke(state)

    async def stream_events(
            self,
            state: ExecutionState,
    ) -> AsyncIterator[dict[str, object]]:
        stream_mode: tuple[Literal["tasks", "messages"], ...] = (
            "tasks",
            "messages",
        )
        stream = self._graph.astream(
            cast(Any, state),
            stream_mode=stream_mode,
            version="v2",
        )
        async with aclosing(stream):
            async for event in stream:
                yield event


def build_runtime(settings: Settings) -> Runtime:
    router = Router(
        model_list=[
            {
                "model_name": settings.llm_model,
                "litellm_params": {
                    "model": f"ollama_chat/{settings.llm_model}",
                    "api_base": settings.model_base_url,
                    "think": settings.llm_answer_think,
                },
            },
        ],
        num_retries=settings.llm_max_retries,
        retry_after=settings.llm_retry_after,
        timeout=settings.llm_timeout,
    )
    structured_router = Router(
        model_list=[
            {
                "model_name": settings.llm_model,
                "litellm_params": {
                    "model": f"ollama_chat/{settings.llm_model}",
                    "api_base": settings.model_base_url,
                    "think": False,
                },
            },
        ],
        num_retries=settings.llm_max_retries,
        retry_after=settings.llm_retry_after,
        timeout=settings.llm_timeout,
    )
    model = ChatLiteLLMRouter(
        router=router,
        model_name=settings.llm_model,
        streaming=True,
    )
    structured_model = ChatLiteLLMRouter(
        router=structured_router,
        model_name=settings.llm_model,
        streaming=True,
    )
    nodes = ResearchGraphNodes(
        routing_step=RoutingStep(model=structured_model),
        mode_selection_step=ModeSelectionStep(model=structured_model),
        clarification_step=ClarificationStep(model=model),
        out_of_scope_step=OutOfScopeStep(model=model),
        answer_step=AnswerStep(model=model),
        documents_context=DocumentsContextService(),
        web_context=WebContextService(),
    )

    return Runtime(graph=build_research_graph(nodes))


@lru_cache
def get_runtime() -> Runtime:
    return build_runtime(get_settings())
