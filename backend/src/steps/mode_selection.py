from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import RunnableConfig

from src.dataclasses.state import ExecutionState
from src.prompts.structural import MODE_SELECTION_PROMPT
from src.schemas.decisions import ModeDecision


class ModeSelectionStep:
    def __init__(self, *, model: BaseChatModel) -> None:
        self._chain = MODE_SELECTION_PROMPT | model.with_structured_output(
            ModeDecision,
            method="json_mode",
        )

    async def select(
        self,
        *,
        state: ExecutionState,
        config: RunnableConfig | None = None,
    ) -> ModeDecision:
        response = await self._chain.ainvoke(
            {
                "question": state.question,
                "chat_history": state.history_messages,
            },
            config=config,
        )
        return ModeDecision.model_validate(response)
