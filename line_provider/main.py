from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from tortoise import Tortoise

from routers.event_routers import event_router
from tortoise_conf import TORTOISE_ORM


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


async def init_db():
    await Tortoise.init(TORTOISE_ORM)
    await Tortoise.generate_schemas()

app = FastAPI(lifespan=lifespan)

app.include_router(event_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info", lifespan='on')
