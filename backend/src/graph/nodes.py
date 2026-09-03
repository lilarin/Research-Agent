import asyncio

from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from src.dataclasses.state import ExecutionState
from src.graph.transitions import ResearchGraphTransitions
from src.services.documents_context import DocumentsContextService
from src.services.web_context import WebContextService
from src.steps.answer import AnswerStep
from src.steps.clarification import ClarificationStep
from src.steps.mode_selection import ModeSelectionStep
from src.steps.out_of_scope import OutOfScopeStep
from src.steps.routing import RoutingStep


class ResearchGraphNodes:
    def __init__(
            self,
            *,
            routing_step: RoutingStep,
            mode_selection_step: ModeSelectionStep,
            clarification_step: ClarificationStep,
            out_of_scope_step: OutOfScopeStep,
            answer_step: AnswerStep,
            documents_context: DocumentsContextService,
            web_context: WebContextService,
    ) -> None:
        self._routing_step = routing_step
        self._mode_selection_step = mode_selection_step
        self._clarification_step = clarification_step
        self._out_of_scope_step = out_of_scope_step
        self._answer_step = answer_step
        self._documents_context = documents_context
        self._web_context = web_context
        self._transitions = ResearchGraphTransitions()

    async def route(
            self, state: ExecutionState, config: RunnableConfig,
    ) -> Command[str]:
        decision = await self._routing_step.route(state=state, config=config)
        return self._transitions.route_start_command(decision=decision)

    async def clarify(
            self, state: ExecutionState, config: RunnableConfig,
    ) -> dict[str, str]:
        answer = await self._clarification_step.clarify(state=state, config=config)
        return {"answer": answer}

    async def out_of_scope(
            self, state: ExecutionState, config: RunnableConfig,
    ) -> dict[str, str]:
        answer = await self._out_of_scope_step.respond(state=state, config=config)
        return {"answer": answer}

    async def select_mode(
            self, state: ExecutionState, config: RunnableConfig,
    ) -> Command[str]:
        decision = await self._mode_selection_step.select(state=state, config=config)
        return self._transitions.select_mode_command(decision=decision)

    async def retrieve_documents(self, state: ExecutionState) -> dict[str, object]:
        return {"context": await self._documents_context.retrieve(state)}

    async def retrieve_web(self, state: ExecutionState) -> dict[str, object]:
        return {"context": await self._web_context.retrieve(state)}

    async def retrieve_documents_and_web(
            self,
            state: ExecutionState,
    ) -> dict[str, object]:
        documents, web = await asyncio.gather(
            self._documents_context.retrieve(state),
            self._web_context.retrieve(state),
        )
        return {"context": [*documents, *web]}

    async def answer(
            self, state: ExecutionState, config: RunnableConfig,
    ) -> dict[str, str]:
        answer = await self._answer_step.execute(state=state, config=config)
        return {"answer": answer}
