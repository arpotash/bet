import fastapi
import uvicorn
from payment.app.routers import payment_router
from tortoise.contrib.fastapi import register_tortoise


app = fastapi.FastAPI()
app.include_router(payment_router)

register_tortoise(
    app,
    db_url="postgres://postgres:postgres@localhost:5432/betting",
    modules={"models": ["payment.app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
