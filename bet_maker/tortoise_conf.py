from config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.db_uri},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
