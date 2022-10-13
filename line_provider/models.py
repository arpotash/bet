from enum import IntEnum
from tortoise import fields
from tortoise.models import Model


class EventStatus(IntEnum):
    new = 1
    home_win = 2
    away_win = 3


class Event(Model):
    uuid = fields.UUIDField(pk=True)
    ratio = fields.DecimalField(decimal_places=2, max_digits=4)
    created = fields.DatetimeField(auto_now_add=True)
    deadline = fields.TimeDeltaField()
    status = fields.IntEnumField(
        EventStatus, required=True, default=EventStatus.new, related_name='event_status'
    )
