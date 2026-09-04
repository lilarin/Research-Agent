import json
from dataclasses import asdict

from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import RunnableConfig

from src.dataclasses.state import ExecutionState
from src.prompts.streaming import ANSWER_PROMPT
from src.utils.time import current_datetime


class AnswerStep:
    def __init__(self, *, model: BaseChatModel) -> None:
        self._chain = ANSWER_PROMPT | model

    async def execute(
            self,
            *,
            state: ExecutionState,
            config: RunnableConfig | None = None,
    ) -> str:
        context = json.dumps(
            [asdict(chunk) for chunk in state.context],
            ensure_ascii=False,
        )
        response = await self._chain.ainvoke(
            {
                "question": state.question,
                "chat_history": state.history_messages,
                "context": context,
                "current_datetime": current_datetime(),
            },
            config=config,
        )
        return response.text
