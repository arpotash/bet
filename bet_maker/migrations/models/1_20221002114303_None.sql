-- upgrade --
CREATE TABLE IF NOT EXISTS "bet" (
    "uuid" UUID NOT NULL  PRIMARY KEY,
    "event_uuid" UUID NOT NULL,
    "bet" DECIMAL(4,2) NOT NULL,
    "status" SMALLINT NOT NULL  DEFAULT 1
);
COMMENT ON COLUMN "bet"."status" IS 'uncompleted: 1\nwin: 2\nlose: 3';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
