import asyncio
import fastapi
from tortoise import Tortoise

from event_deadline_checker.app.services import PaymentOperation
from event_deadline_checker.tortoise_conf import TORTOISE_ORM

app = fastapi.FastAPI()


async def init_db():
    await Tortoise.init(TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def check_winner_bets():
    await init_db()

    await PaymentOperation.increase_balance_winner_user()

if __name__ == "__main__":
    asyncio.run(check_winner_bets())
