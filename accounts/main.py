import asyncio
import nest_asyncio

import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from accounts.routers.auth import auth_router
from accounts.resources.broker import read_kafka

nest_asyncio.apply()

app = FastAPI()


app.include_router(auth_router)

register_tortoise(
    app,
    db_url="postgres://postgres:postgres@localhost:5432/betting",
    modules={"models": ["accounts.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


async def run_uvicorn():
    config = uvicorn.Config(app, port=8002, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    loop = asyncio.get_event_loop()
    coroutines = [read_kafka(), run_uvicorn()]
    loop.run_until_complete(asyncio.gather(*coroutines))


if __name__ == "__main__":
    asyncio.run(main())
