import fastapi
from fastapi import APIRouter
from payment.app.dependecies import AuthRequired
from payment.app.schemas import CardSchemas
from payment.resources.broker import Producer
from payment.app.models import Card

payment_router = APIRouter(prefix="", tags=["payment"])


@payment_router.post(
    "/withdrawal",
    status_code=fastapi.status.HTTP_201_CREATED
)
async def withdrawal_payment(
        card_schema: CardSchemas,
        user: AuthRequired = fastapi.Depends(AuthRequired.handle)):
    card = await Card.get(id=card_schema.uuid)
    body = {"card": card_schema.uuid, "user": user.uuid, "action": "increase", "bet": card_schema.amount}
    try:
        await card.decrease_balance(card_schema.amount)
    except ValueError:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_406_NOT_ACCEPTABLE,
            detail="Not enough money"
        )
    else:
        await Producer.produce("payment", body)


@payment_router.post(
    "/increase",
    status_code=fastapi.status.HTTP_201_CREATED
)
async def increase_balance(
        card_schema: CardSchemas,
        user: AuthRequired = fastapi.Depends(AuthRequired.handle)
):
    card = await Card.get_or_none(id=card_schema.uuid)
    body = {"card": card_schema.uuid, "user": user, "action": "decrease", "bet": card_schema.amount}
    await Producer.produce("payment", body)
    await card.decrease_balance(card_schema.amount)
