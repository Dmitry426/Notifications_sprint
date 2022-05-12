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


class MailSettings(BaseSettings):
    from_mail = "pastseason.ru@gmail.com"
    mail_password = "lzimqxbqvzxukjnv"
    mail_smtp = "smtp.gmail.com"
    mail_smtp_port = "587"
    bitly_access_token = "0fdd2a8c607818857db17b6109a94de801427a6d"


class Postgres(BaseSettings):
    class Config:
        env_prefix = "PG_"

    user = "user"
    dbname = " name"
    password = "password"
    host = "postgres"
    port = "5432"


class Settings(RabbitSettings, MailSettings, Postgres):
    """Represents ETL settings."""

    class Config:
        env_prefix = "WORKER_"

    queue: str = "film"


settings = Settings()
