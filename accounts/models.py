import datetime
import uuid

from tortoise import fields
from tortoise.models import Model


class User(Model):
    """
    User model
    """

    id = fields.UUIDField(pk=True, default=uuid.uuid4())
    salt = fields.CharField(max_length=128, null=False)
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    register_date = fields.DateField(default=datetime.date.today())
    email = fields.CharField(max_length=128, null=False)
    password = fields.CharField(max_length=256, null=False)
    is_active = fields.BooleanField(null=False, default=True)
    is_verified = fields.BooleanField(null=False, default=False)

    class Meta:
        table: str = "accounts"

    def __str__(self):
        return self.email
