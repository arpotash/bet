import typing
import uuid

import fastapi
import tortoise.exceptions
from tortoise.functions import Trim
from fastapi import APIRouter, status
from bet_maker.app.models import Bet, BetStatus
from bet_maker.core.config import settings
from bet_maker.app.dependencies.auth import AuthRequired
from bet_maker.app.schemas import BetCreate, BetStatusUpdate, bet_pydantic_model
from bet_maker.app.resources.broker import Producer
from bet_maker.app.services import Bet as bet_service
import httpx

bet_maker_router = APIRouter(prefix="", tags=["bet-maker"])


@bet_maker_router.post(
    "/bet",
    status_code=status.HTTP_201_CREATED,
)
async def create_ordinary_bet(bet: BetCreate, user=fastapi.Depends(AuthRequired.handle)):
    events = []
    for event in bet.event_uuid_lst:
        try:
            response = httpx.get(url=f"{settings.event_get_route}{event}")
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        else:
            events.append(response.json())
    bet_instance = bet_service(bet.model_dump(), events, user.get("id"))
    await bet_instance.create()


@bet_maker_router.get(
    "/bets",
    status_code=status.HTTP_200_OK,
    dependencies=[fastapi.Depends(AuthRequired.handle)]
)
async def get_bets():
    return await bet_pydantic_model.from_queryset(Bet.all())


@bet_maker_router.get(
    "/bets/{uuid}",
    dependencies=[fastapi.Depends(AuthRequired.handle)]
)
async def get_event_bet(uuid: str):
    return await bet_pydantic_model.from_queryset_single(Bet.get(uuid=uuid))


@bet_maker_router.put(
    "/bets/{uuid}",
)
async def sell_bet(uuid: str, user=fastapi.Depends(AuthRequired.handle)):
    try:
        bet_query = Bet.get(uuid=uuid)
        bet = await bet_query
    except tortoise.exceptions.DoesNotExist as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Bet not found"
        )
    else:
        bet.status = BetStatus.sold
        await bet.save()
        await Producer.produce("payment", dict(action="increase", bet=float(bet.bet), user=user))
        return await bet_pydantic_model.from_queryset_single(bet_query)


@bet_maker_router.get(
    "/events_bet"
)
async def get_bets_by_events(events: typing.List[uuid.UUID] = fastapi.Query(None)):
    bets = await Bet.filter(events__event__in=events).values(
        "uuid", "user", "bet", "prediction", "ratio", "status", "events__event"
    )
    return bets


@bet_maker_router.patch(
    "/bets/{uuid}/status"
)
async def update_bet_status(uuid: str, bet_status: BetStatusUpdate):
    try:
        bet_query = Bet.get(uuid=uuid)
        bet = await bet_query
    except tortoise.exceptions.DoesNotExist as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Bet not found"
        )
    else:
        bet.status = bet_status.bet_status
        await bet.save()
        return await bet_pydantic_model.from_queryset_single(bet_query)
