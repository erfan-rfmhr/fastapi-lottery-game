import uuid

from pydantic import BaseModel


class UserSchema(BaseModel):
    UUID: uuid.UUID
