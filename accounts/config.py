import os
from typing import Optional

from fastapi_mail import ConnectionConfig
from pydantic import BaseModel


class Settings(BaseModel):
    """
    Конфигурации переменных приложения
    """

    debug: Optional[bool] = True if os.getenv("DEBUG") == "1" else False
    secret: str = os.getenv("SECRET")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    password_salt: Optional[bytes] = os.getenv("PASSWORD_SALT")
    # Database credentials
    db_user: Optional[str] = os.getenv("DB_USER")
    db_password: Optional[str] = os.getenv("DB_PASSWORD")
    db_host: Optional[str] = os.getenv("DB_HOST")
    db_port: Optional[int] = int(os.getenv("DB_PORT", "5432"))
    db_name: Optional[str] = os.getenv("DB_NAME")
    db_uri: Optional[str] = f"postgres://{db_user}:{db_password}@{db_host}/{db_name}"
    # Smtp server credentials
    mail_username: Optional[str] = os.getenv("MAIL_USERNAME")
    mail_password: Optional[str] = os.getenv("MAIL_PASSWORD")
    mail_from: Optional[str] = os.getenv("MAIL_HOST")
    mail_port: Optional[int] = int(os.getenv("MAIL_PORT", "465"))
    mail_server: Optional[str] = os.getenv("MAIL_SERVER")
    mail_tls: Optional[bool] = os.getenv("MAIL_TLS", False)
    mail_ssl: Optional[bool] = os.getenv("MAIL_SSL", True)
    use_credentials: Optional[bool] = os.getenv("USE_CREDENTIALS", True)
    validate_certs: Optional[bool] = os.getenv("VALIDATE_CERTS", True)


settings = Settings()
email_config = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_TLS=settings.mail_tls,
    MAIL_SSL=settings.mail_ssl,
    USE_CREDENTIALS=settings.use_credentials,
    VALIDATE_CERTS=settings.validate_certs,
)