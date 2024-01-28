import datetime

from pydantic import BaseModel
from pydantic.fields import Field

from models import Event, EventStatus
from tortoise.contrib.pydantic import pydantic_model_creator


class EventChangeSuccess(BaseModel):
    message: str = Field(example="Event status has been changed")
    status: EventStatus


class UnavailableService(BaseModel):
    message: str = Field(example="Service unavailable")


class StatusNotFound(BaseModel):
    status: EventStatus
    message: str = Field(example="Status doesn't exist")


class EventRatio(BaseModel):
    ratio: float = Field(example=2.00)


class EventNotFound(BaseModel):
    uuid: str = Field(example=2.00)
    message: str = Field("Event not found")


class EventCreate(BaseModel):
    ratio: float = Field(example=2.00)
    deadline: datetime.datetime = Field()
    status: int = Field(example=1)


event_pydantic_model = pydantic_model_creator(Event, name="event")
