import os
from typing import Optional

from pydantic import BaseModel

from fastapi_mail import ConnectionConfig


class Settings(BaseModel):
    """
    Конфигурации переменных приложения
    """

    debug: Optional[bool] = True if os.getenv("DEBUG") == "1" else False
    secret: str = os.getenv("SECRET", "secret")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    password_salt: Optional[bytes] = os.getenv("PASSWORD_SALT", "salt")
    # Database credentials
    db_user: Optional[str] = os.getenv("DB_USER", "postgres")
    db_password: Optional[str] = os.getenv("DB_PASSWORD", "postgres")
    db_host: Optional[str] = os.getenv("DB_HOST", "127.0.0.1")
    db_port: Optional[int] = int(os.getenv("DB_PORT", "5432"))
    db_name: Optional[str] = os.getenv("DB_NAME", "betting")
    db_uri: Optional[str] = f"postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    # Smtp server credentials
    mail_username: Optional[str] = os.getenv("MAIL_USERNAME", "testusername")
    mail_password: Optional[str] = os.getenv("MAIL_PASSWORD", "testpassword")
    mail_from: Optional[str] = os.getenv("MAIL_HOST", "testmail@gmail.com")
    mail_port: Optional[int] = int(os.getenv("MAIL_PORT", "465"))
    mail_server: Optional[str] = os.getenv("MAIL_SERVER", "testmail@gmail.com")
    mail_start_tls: Optional[bool] = os.getenv("MAIL_TLS", False)
    mail_ssl_tls: Optional[bool] = os.getenv("MAIL_SSL", True)
    use_credentials: Optional[bool] = os.getenv("USE_CREDENTIALS", True)
    validate_certs: Optional[bool] = os.getenv("VALIDATE_CERTS", True)


settings = Settings()
email_config = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=settings.mail_start_tls,
    MAIL_SSL_TLS=settings.mail_ssl_tls,
    USE_CREDENTIALS=settings.use_credentials,
    VALIDATE_CERTS=settings.validate_certs,
)
