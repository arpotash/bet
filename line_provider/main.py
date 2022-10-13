from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from line_provider.routers.event_routers import event_router

app = FastAPI()

app.include_router(event_router)

register_tortoise(
    app,
    db_url='postgres://postgres:postgres@localhost:5432/events',
    modules={'models': ['line_provider.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)
