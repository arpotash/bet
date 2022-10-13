-- upgrade --
CREATE TABLE IF NOT EXISTS "event" (
    "uuid" UUID NOT NULL  PRIMARY KEY,
    "ratio" DECIMAL(4,2) NOT NULL,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deadline" BIGINT NOT NULL,
    "status" SMALLINT NOT NULL  DEFAULT 1
);
COMMENT ON COLUMN "event"."status" IS 'new: 1\nhome_win: 2\naway_win: 3';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
