import fastapi
import tortoise

from uuid import UUID
from tortoise.transactions import in_transaction
from bet_maker.app.models import Bet as bet_model, BetEvent as bet_event_model



class Bet:

    def __init__(self, bet_data: dict, events: list, user: UUID):
        self.bet_data = bet_data
        self.events = events
        self.user = user

    async def prepare_events(self, bet_uuid: UUID) -> list:
        events = []
        for event in self.events:
            events.append(bet_event_model(
                event=event.get("uuid"), bet=bet_uuid, user=self.user, ratio=event.get("ratio"))
            )
        return events

    @staticmethod
    async def calculate_express_ratio(events: list):
        ratio = 1
        for event in events:
            ratio *= float(event.get("ratio"))
        return ratio

    async def add_event_to_bet(self, bet_uuid):
        events = await self.prepare_events(bet_uuid)
        await bet_event_model.bulk_create(events)

    async def create(self) -> bet_model:
        self.bet_data.pop("event_uuid_lst")
        async with in_transaction("default") as connection:
            try:
                total_ratio = await self.calculate_express_ratio(self.events)
                self.bet_data["ratio"] = total_ratio
                bet = await bet_model.create(**self.bet_data)
                await self.add_event_to_bet(bet)
            except Exception as e:
                await connection.rollback()
            else:
                return bet

    async def update_status(self):
        try:
            bet_query = bet_model.get(uuid=self.bet_data.get("uuid"))
            bet = await bet_query
        except tortoise.exceptions.DoesNotExist as exc:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail="Bet not found"
            )
        else:
            bet.status = self.bet_data.get("status")
            await bet.save()
