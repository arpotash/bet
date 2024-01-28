import datetime
from uuid import UUID
from enum import IntEnum

from tortoise import fields
from tortoise.models import Model


class EventStatus(IntEnum):
    new = 1
    home_win = 2
    away_win = 3
    draw = 4


class Event(Model):
    uuid = fields.UUIDField(pk=True)
    created = fields.DatetimeField(auto_now_add=True, null=True)
    deadline: datetime.datetime = fields.DatetimeField()
    ratio = fields.DecimalField(decimal_places=2, max_digits=6, required=True)
    status = fields.IntEnumField(
        EventStatus, required=True, default=EventStatus.new, related_name="event_status"
    )
