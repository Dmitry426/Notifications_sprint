from uuid import uuid4

from pydantic import Field
from pydantic.validators import UUID

from ..models.base import JsonConfig, Letter


class UserAuth(JsonConfig):
    id: UUID = Field(default_factory=uuid4)
    email: str
    link_out: str
    link: str
    user: str


class WellcomeLetter(Letter):
    subject: str = "Wellcome Letter"
