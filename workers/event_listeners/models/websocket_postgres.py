from uuid import uuid4

from pydantic import Field, BaseModel
from pydantic.validators import UUID


class User(BaseModel):
    id_: UUID = Field(default_factory=uuid4)
    user_id: UUID
    body: str
    is_read: bool = Field(default_factory=False)
