from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import RunnableConfig

from src.dataclasses.state import ExecutionState
from src.prompts.streaming import OUT_OF_SCOPE_PROMPT


class OutOfScopeStep:
    def __init__(self, *, model: BaseChatModel) -> None:
        self._chain = OUT_OF_SCOPE_PROMPT | model

    async def respond(
        self,
        *,
        state: ExecutionState,
        config: RunnableConfig | None = None,
    ) -> str:
        response = await self._chain.ainvoke(
            {
                "question": state.question,
            },
            config=config,
        )
        return response.text
