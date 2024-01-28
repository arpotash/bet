from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "event" (
    "uuid" UUID NOT NULL  PRIMARY KEY,
    "created" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "deadline" TIMESTAMPTZ NOT NULL,
    "ratio" DECIMAL(6,2) NOT NULL,
    "status" SMALLINT NOT NULL  DEFAULT 1
);
COMMENT ON COLUMN "event"."status" IS 'new: 1\nhome_win: 2\naway_win: 3\ndraw: 4';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
