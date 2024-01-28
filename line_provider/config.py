import os
from typing import Optional

from pydantic import BaseModel

from fastapi_mail import ConnectionConfig


class Settings(BaseModel):
    """
    Конфигурации переменных приложения
    """

    debug: Optional[bool] = True if os.getenv("DEBUG") == "1" else False
    secret: str = os.getenv("SECRET")
    # Database credentials
    db_user: Optional[str] = os.getenv("DB_USER", "postgres")
    db_password: Optional[str] = os.getenv("DB_PASSWORD", "postgres")
    db_host: Optional[str] = os.getenv("DB_HOST", "localhost")
    db_port: Optional[int] = int(os.getenv("DB_PORT", "5432"))
    db_name: Optional[str] = os.getenv("DB_NAME", "betting")
    db_uri: Optional[str] = f"postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


settings = Settings()
