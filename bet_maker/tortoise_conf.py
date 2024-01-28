from bet_maker.core.config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.db_uri},
    "apps": {
        "models": {
            "models": ["bet_maker.app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
