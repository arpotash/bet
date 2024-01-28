from fastapi import FastAPI
import uvicorn
from bet_maker.app.routers import bet_maker_router
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

app.include_router(bet_maker_router)

register_tortoise(
    app,
    db_url="postgres://postgres:postgres@localhost:5432/betting",
    modules={"models": ["bet_maker.app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info", lifespan='on')
