from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class CommentCreate(BaseModel):
    text: str


class CommentResponse(BaseModel):
    id: UUID
    text: str
    created_at: datetime
    author_id: UUID

    class Config:
        orm_mode = True

