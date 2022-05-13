from uuid import uuid4

from pydantic import BaseModel, Field
from pydantic.validators import UUID

from workers.event_listeners.models.base import JsonConfig


class User(BaseModel):
    name: str
    email: str


class Bookmark(JsonConfig):
    id: UUID = Field(default_factory=uuid4)
    link_out: str
    link: str
    serial_name: str
    users: list[User]


class BookmarkTemplateData(JsonConfig):
    link_out: str
    link: str
    user: str
    serial_name: str
