from uuid import uuid4

from pydantic import BaseModel, Field
from pydantic.validators import UUID


class UserWebsock(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    body: str
    is_read: bool = False
