-- upgrade --
CREATE TABLE IF NOT EXISTS "accounts" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "salt" VARCHAR(128) NOT NULL,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "register_date" DATE NOT NULL  DEFAULT '2022-10-02',
    "email" VARCHAR(128) NOT NULL,
    "password" VARCHAR(256) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_verified" BOOL NOT NULL  DEFAULT False
);
COMMENT ON TABLE "accounts" IS 'Модель пользователя';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
