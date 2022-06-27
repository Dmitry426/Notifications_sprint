__all__ = ["settings"]

from pydantic import BaseSettings


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

    user: str = "postgres"
    dbname: str = "notifications"
    password: str = "password_user"
    host: str = "postgres"
    port: str = "5432"


class MailSettings(BaseSettings):
    """ Represents mailing settings."""
    class Config:
        env_prefix = "BITLY_"

    access_token = "0fdd2a8c607818857db17b6109a94de801427a6d"


class Settings(RabbitSettings):
    """Represents all settings."""
    rabbit: RabbitSettings = RabbitSettings()
    postgres: Postgres = Postgres()
    mail: MailSettings = MailSettings()
    backoff_timeout: int = 30


settings = Settings()
