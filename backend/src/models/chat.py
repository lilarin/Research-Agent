from tortoise import fields
from tortoise.models import Model

from src.enums.messages import MessageRole


class ChatMessage(Model):
    id = fields.BigIntField(primary_key=True)
    conversation_uuid = fields.UUIDField()
    role = fields.CharEnumField(MessageRole, max_length=16)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "chat_messages"
        ordering = ["created_at", "id"]
        indexes = [
            ("conversation_uuid", "created_at", "id"),
        ]
