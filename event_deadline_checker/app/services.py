import datetime
import random
import typing

import httpx

from event_deadline_checker.app.models import Event, EventStatus
from event_deadline_checker.core.config import settings
from event_deadline_checker.resources.broker import Producer


class EventOperation:

    @classmethod
    async def check_event_deadline(cls) -> list:
        finished_events = await Event.filter(
            deadline__lte=datetime.datetime.now(),
            status=EventStatus.new
        )
        return finished_events

    @classmethod
    async def update_status(cls, events: list) -> None:
        event_uuid_lst = []
        for event in events:
            event.status = random.choice([EventStatus.draw, EventStatus.away_win, EventStatus.home_win])
            event_uuid_lst.append(event.uuid)
            await event.save()


class BetOperation:

    @classmethod
    async def get_bet_by_event(cls, events):

        if not events:
            return []

        query_params = {"events": events}
        response = httpx.get(url=settings.bets_by_events_url, params=query_params)
        response.raise_for_status()

        return response.json()

    @classmethod
    async def update_bet_status(cls, bets):
        await Producer.produce("bet_status", bets)


class PaymentOperation:

    @classmethod
    def check_equal_prediction_result(cls, prediction: int, result: int):
        return prediction == result

    @classmethod
    async def increase_balance_winner_user(cls):
        events = await EventOperation.check_event_deadline()
        await EventOperation.update_status(events)
        events_uuid_lst = [event.uuid for event in events]
        bets = await BetOperation.get_bet_by_event(events_uuid_lst)
        await BetOperation.update_bet_status(bets)
        for bet in bets:
            event_status = [event.status for event in events if event.status == bet.get("prediction")]
            if event_status and cls.check_equal_prediction_result(bet.get("prediction"), event_status[0]):
                body = {"user": bet.get("user"), "action": "increase", "bet": bet.get("bet")}
                await Producer.produce("payment", body)
