__all__ = ["settings"]

from pydantic import BaseSettings


class MailSettings(BaseSettings):
    class Config:
        env_prefix = "EMAIL_"

    email_from = "pastseason.ru@gmail.com"
    password = "lzimqxbqvzxukjnv"
    smtp = "smtp.gmail.com"
    smtp_port = "587"


class Websocket(BaseSettings):
    class Config:
        env_prefix = "WEBSOCKET_"

    host = "0.0.0.0"
    port = 8765


class RabbitSettings(BaseSettings):
    """Represents Kafka settings."""

    class Config:
        env_prefix = "RABBIT_"

    host: str = "localhost"
    name: str = "user1"
    password: str = "pass1"


class Postgres(BaseSettings):
    """Represents Postgres settings."""

    class Config:
        env_prefix = "POSTGRES_"

    user: str
    dbname: str = "notifications"
    password: str = "password_user"
    host: str = "postgres"
    port: str = "5432"


class Settings(RabbitSettings):
    """Represents all settings."""
    rabbit: RabbitSettings = RabbitSettings()
    postgres: Postgres = Postgres()
    mail: MailSettings = MailSettings()
    websocket: Websocket = Websocket()
    backoff_timeout: int = 30


settings = Settings()
