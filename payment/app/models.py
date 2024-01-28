import uuid

from tortoise import fields
from tortoise.models import Model


class Card(Model):
    """
    Card user model
    """
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    user = fields.UUIDField(null=False)
    number = fields.CharField(max_length=128, null=False)
    expiration_date = fields.DateField(null=False)
    owner = fields.CharField(max_length=128, null=False)
    balance = fields.DecimalField(default=0, decimal_places=2, max_digits=10)

    class Meta:
        table: str = "cards"

    def __str__(self):
        return self.number

    def check_balance(self, amount: float):
        if self.balance < amount:
            raise ValueError("Insufficient funds")

    async def increase_balance(self, amount: float):
        self.balance = float(self.balance) + amount
        await self.save()

    async def decrease_balance(self, amount: float):
        self.check_balance(amount)
        self.balance = float(self.balance) - amount
        await self.save()
