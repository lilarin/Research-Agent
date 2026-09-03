from collections.abc import AsyncIterator
from contextlib import aclosing
from functools import lru_cache

from langchain_ollama import ChatOllama
from langgraph.graph.state import CompiledStateGraph

from app.config import Settings, get_settings
from src.dataclasses.state import ExecutionState
from src.enums.nodes import GraphNode
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

    async def stream(
            self,
            state: ExecutionState,
    ) -> AsyncIterator[str]:
        stream = self._graph.astream(state, stream_mode="messages")
        async with aclosing(stream):
            async for message, metadata in stream:
                if metadata["langgraph_node"] not in (
                        GraphNode.ANSWER,
                        GraphNode.CLARIFY,
                        GraphNode.OUT_OF_SCOPE,
                ):
                    continue
                text = message.text
                if text:
                    yield text


def build_runtime(settings: Settings) -> Runtime:
    model = ChatOllama(
        base_url=settings.model_base_url,
        model=settings.llm_model,
    )
    nodes = ResearchGraphNodes(
        routing_step=RoutingStep(model=model),
        mode_selection_step=ModeSelectionStep(model=model),
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
