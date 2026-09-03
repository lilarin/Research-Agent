from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import RunnableConfig

from src.dataclasses.state import ExecutionState
from src.prompts.streaming import CLARIFICATION_PROMPT


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
            },
            config=config,
        )
        return response.text
