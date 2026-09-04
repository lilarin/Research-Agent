from tortoise import BaseDBAsyncClient


RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
            "id" BIGSERIAL NOT NULL PRIMARY KEY,
            "version" VARCHAR(255) NOT NULL,
            "app" VARCHAR(100) NOT NULL,
            "content" JSONB NOT NULL
        );
        CREATE TABLE IF NOT EXISTS "chat_messages" (
            "id" BIGSERIAL NOT NULL PRIMARY KEY,
            "conversation_uuid" UUID NOT NULL,
            "role" VARCHAR(16) NOT NULL,
            "content" TEXT NOT NULL,
            "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS "idx_chat_messages_conversation_uuid"
            ON "chat_messages" ("conversation_uuid");
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "chat_messages";
    """
