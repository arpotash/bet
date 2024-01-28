from payment.core.config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.db_uri},
    "apps": {
        "models": {
            "models": ["payment.app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
