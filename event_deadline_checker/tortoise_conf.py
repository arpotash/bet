from event_deadline_checker.core.config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.db_uri},
    "apps": {
        "models": {
            "models": ["event_deadline_checker.app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
