from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    name: Optional[str] = None
    slack_id: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None


class UserOut(UserBase):
    id: UUID
    created_at: Optional[datetime]

    model_config = {"from_attributes": True}
