from datetime import datetime

from pydantic.validators import UUID, Enum

from workers.event_listeners.models.base import JsonConfig


class Choices(Enum):
    sms = "sms"
    email = "email"
    websocket = "websocket"


class User(JsonConfig):
    id: UUID
    email: str
    FirstName: str
    LastName: str
    ContactType: Choices
    created: datetime
