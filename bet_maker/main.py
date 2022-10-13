from fastapi import FastAPI

from bet_maker.routers import bet_maker_router
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

app.include_router(bet_maker_router)

register_tortoise(
    app,
    db_url="postgres://postgres:postgres@localhost:5432/betting",
    modules={"models": ["bet_maker.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
