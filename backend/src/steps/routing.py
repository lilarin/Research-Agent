from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import RunnableConfig

from src.dataclasses.state import ExecutionState
from src.prompts.structural import ROUTE_PROMPT
from src.schemas.decisions import RouteDecision


class RoutingStep:
    def __init__(self, *, model: BaseChatModel) -> None:
        self._chain = ROUTE_PROMPT | model.with_structured_output(
            RouteDecision,
            method="json_mode",
        )

    async def route(
        self,
        *,
        state: ExecutionState,
        config: RunnableConfig | None = None,
    ) -> RouteDecision:
        response = await self._chain.ainvoke(
            {
                "question": state.question,
                "chat_history": state.history_messages,
            },
            config=config,
        )
        return RouteDecision.model_validate(response)
