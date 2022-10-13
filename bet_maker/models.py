from enum import IntEnum

from tortoise import fields
from tortoise.models import Model


class BetStatus(IntEnum):
    uncompleted = 1
    win = 2
    lose = 3


class Bet(Model):
    uuid = fields.UUIDField(pk=True)
    event_uuid = fields.UUIDField(required=True)
    bet = fields.DecimalField(decimal_places=2, max_digits=4, required=True)
    status = fields.IntEnumField(
        BetStatus,
        required=True,
        default=BetStatus.uncompleted,
        related_name="bet_status",
    )
