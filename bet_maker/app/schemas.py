from typing import List
from pydantic import BaseModel
from pydantic.fields import Field
from bet_maker.app.models import Bet, BetStatus
from tortoise.contrib.pydantic import pydantic_model_creator


class BetCreate(BaseModel):
    event_uuid_lst: List[str] = Field(
        example=["3fe92ce6-54f3-4560-901b-bf53f50829c3", "8bf699f8-dc28-4254-9648-8c27afb2ad12"]
    )
    bet_type: str = Field(example="ordinary", default="ordinary")
    bet: float = Field(example=100)


class BetStatusUpdate(BaseModel):
    bet_status: int = Field(example=1)


bet_pydantic_model = pydantic_model_creator(Bet, name="bet")
