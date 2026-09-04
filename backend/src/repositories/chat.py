from uuid import UUID

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from tortoise.transactions import in_transaction

from src.enums.messages import MessageRole
from src.models.chat import ChatMessage


class ChatHistoryRepository:
    def __init__(self, *, messages_limit: int) -> None:
        self._messages_limit = messages_limit

    async def get(self, conversation_uuid: UUID) -> list[BaseMessage]:
        messages = await ChatMessage.filter(
            conversation_uuid=conversation_uuid,
        ).order_by(
            "-created_at",
            "-id",
        ).limit(self._messages_limit)
        messages.reverse()
        return [self._to_message(message.role, message.content) for message in messages]

    @staticmethod
    async def append(
            *,
            conversation_uuid: UUID,
            question: str,
            answer: str,
    ) -> None:
        async with in_transaction() as connection:
            await ChatMessage.create(
                conversation_uuid=conversation_uuid,
                role=MessageRole.HUMAN,
                content=question,
                using_db=connection,
            )
            await ChatMessage.create(
                conversation_uuid=conversation_uuid,
                role=MessageRole.AI,
                content=answer,
                using_db=connection,
            )

    @staticmethod
    def _to_message(role: str, content: str) -> BaseMessage:
        if role == MessageRole.HUMAN:
            return HumanMessage(content=content)
        return AIMessage(content=content)
