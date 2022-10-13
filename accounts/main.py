from fastapi import FastAPI

from accounts.routers import auth_router
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

app.include_router(auth_router)

register_tortoise(
    app,
    db_url="postgres://postgres:postgres@localhost:5432/accounts",
    modules={"models": ["accounts.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
