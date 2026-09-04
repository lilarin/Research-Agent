from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import RunnableConfig

from src.dataclasses.state import ExecutionState
from src.prompts.streaming import CLARIFICATION_PROMPT
from src.utils.time import current_datetime


class ClarificationStep:
    def __init__(self, *, model: BaseChatModel) -> None:
        self._chain = CLARIFICATION_PROMPT | model

    async def clarify(
            self,
            *,
            state: ExecutionState,
            config: RunnableConfig | None = None,
    ) -> str:
        response = await self._chain.ainvoke(
            {
                "question": state.question,
                "chat_history": state.history_messages,
                "current_datetime": current_datetime(),
            },
            config=config,
        )
        return response.text
