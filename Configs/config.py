__all__ = ["settings"]

from pydantic import BaseSettings


class RabbitSettings(BaseSettings):
    class Config:
        env_prefix = "RABBIT"

    r_host: str = "192.168.5.35"
    r_backoff_timeout: int = 30
    r_name: str = "user1"
    r_password: str = "pass1"
    from_mail = "pastseason.ru@gmail.com"
    mail_password = "lzimqxbqvzxukjnv"
    mail_smtp = "smtp.gmail.com"
    mail_smtp_port = "587"
    bitly_access_token = "0fdd2a8c607818857db17b6109a94de801427a6d"


settings = RabbitSettings()
