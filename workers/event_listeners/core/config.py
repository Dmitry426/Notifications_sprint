__all__ = ["settings"]

from pydantic import BaseSettings


class RabbitSettings(BaseSettings):
    """Represents Kafka settings."""

    class Config:
        env_prefix = "RABBIT_"

    r_host: str = "localhost"
    r_backoff_timeout: int = 30
    r_name: str = "user1"
    r_password: str = "pass1"


class Postgres(BaseSettings):
    """Represents Postgres settings."""

    class Config:
        env_prefix = "PG_"

    user = "user"
    dbname = "notifications"
    password = "password"
    host = "postgres"
    port = "5432"


class MailSettings(BaseSettings):
    bitly_access_token = "0fdd2a8c607818857db17b6109a94de801427a6d"


class Settings(RabbitSettings, Postgres, MailSettings):
    """Represents all settings."""

    class Config:
        env_prefix = "WORKER_"

    max_backoff: int = 30


settings = Settings()
