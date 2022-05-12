__all__ = ["settings"]

from pydantic import BaseSettings


class RabbitSettings(BaseSettings):
    """Represents Kafka settings."""

    class Config:
        env_prefix = "WORKER_"

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


class Settings(RabbitSettings, Postgres):
    """Represents all settings."""

    class Config:
        env_prefix = "WORKER_"

    queue: str = "film"


settings = Settings()
