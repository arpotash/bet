from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "accounts" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "salt" VARCHAR(128) NOT NULL,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "balance" DECIMAL(10,2) NOT NULL  DEFAULT 0,
    "register_date" DATE NOT NULL  DEFAULT '2024-01-05',
    "email" VARCHAR(128) NOT NULL,
    "password" VARCHAR(256) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_verified" BOOL NOT NULL  DEFAULT False
);
COMMENT ON TABLE "accounts" IS 'User model';
CREATE TABLE IF NOT EXISTS "cards" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "number" VARCHAR(128) NOT NULL,
    "expiration_date" DATE NOT NULL,
    "owner" VARCHAR(128) NOT NULL,
    "user_id" UUID NOT NULL REFERENCES "accounts" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "cards" IS 'Card user model';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
