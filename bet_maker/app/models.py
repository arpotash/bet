from enum import IntEnum

from uuid import uuid4
from tortoise import fields
from tortoise.models import Model


class BetStatus(IntEnum):
    uncompleted = 1
    win = 2
    lose = 3
    refund = 4
    sold = 5


class SubBetStatus(IntEnum):
    uncompleted = 1
    win = 2
    lose = 3


class BetResult(IntEnum):
    home_win = 2
    away_win = 3
    draw = 4


class Bet(Model):
    uuid = fields.UUIDField(pk=True)
    events = fields.ManyToManyField('models.BetEvent', related_name="events", through="betevent")
    user = fields.UUIDField(default=uuid4)
    bet = fields.DecimalField(decimal_places=2, max_digits=6, required=True)
    prediction = fields.IntEnumField(
        BetResult,
        required=True,
        related_name="bet_prediction"
    )
    ratio = fields.DecimalField(decimal_places=2, max_digits=6, required=True)
    status = fields.IntEnumField(
        BetStatus,
        required=True,
        default=BetStatus.uncompleted,
        related_name="bet_status",
    )


class BetEvent(Model):
    bet = fields.ForeignKeyField('models.Bet', related_name="bet_events")
    event = fields.UUIDField()
    status = fields.IntEnumField(
        SubBetStatus,
        required=True,
        default=BetStatus.uncompleted,
        related_name="sub_bet_status",
    )
