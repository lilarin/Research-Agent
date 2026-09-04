from tortoise import BaseDBAsyncClient


RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "idx_chat_messages_conversation_uuid";
        CREATE INDEX IF NOT EXISTS "idx_chat_messages_conversation_uuid_created_at_id"
            ON "chat_messages" ("conversation_uuid", "created_at", "id");
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "idx_chat_messages_conversation_uuid_created_at_id";
        CREATE INDEX IF NOT EXISTS "idx_chat_messages_conversation_uuid"
            ON "chat_messages" ("conversation_uuid");
    """
