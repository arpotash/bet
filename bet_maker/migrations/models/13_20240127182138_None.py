from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "bet" (
    "uuid" UUID NOT NULL  PRIMARY KEY,
    "user" UUID NOT NULL,
    "bet" DECIMAL(6,2) NOT NULL,
    "prediction" SMALLINT NOT NULL,
    "ratio" DECIMAL(6,2) NOT NULL,
    "status" SMALLINT NOT NULL  DEFAULT 1
);
COMMENT ON COLUMN "bet"."prediction" IS 'home_win: 2\naway_win: 3\ndraw: 4';
COMMENT ON COLUMN "bet"."status" IS 'uncompleted: 1\nwin: 2\nlose: 3\nrefund: 4\nsold: 5';
CREATE TABLE IF NOT EXISTS "betevent" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "event" UUID NOT NULL,
    "status" SMALLINT NOT NULL  DEFAULT 1,
    "bet_id" UUID NOT NULL REFERENCES "bet" ("uuid") ON DELETE CASCADE
);
COMMENT ON COLUMN "betevent"."status" IS 'uncompleted: 1\nwin: 2\nlose: 3';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
