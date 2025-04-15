from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class GroupCreate(BaseModel):
    name: str
    type: str


class GroupResponse(BaseModel):
    id: UUID
    name: str
    type: str
    invite_code: Optional[str]

    class Config:
        orm_mode = True
