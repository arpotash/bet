from fastapi import APIRouter, status

from bet_maker.schemas import Bet

bet_maker_router = APIRouter(prefix="", tags=["bet-maker"])


@bet_maker_router.post("/bet", response_model=status.HTTP_201_CREATED)
async def create_bet():
    pass


@bet_maker_router.get(
    "/bets",
    response_model=status.HTTP_200_OK,
)
async def get_open_bets():
    pass


@bet_maker_router.get("/made_bets", response_model=status.HTTP_200_OK)
async def get_made_bets():
    pass
