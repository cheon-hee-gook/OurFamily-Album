from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.comment import CommentResponse
from app.schemas.tag import TagResponse
from uuid import UUID


class PhotoCreate(BaseModel):
    memo: Optional[str] = ""
    tags: List[str] = []


class PhotoResponse(BaseModel):
    id: UUID
    image_url: str
    memo: Optional[str]
    created_at: datetime
    tags: List[TagResponse] = []
    comments: List[CommentResponse] = []

    class Config:
        orm_mode = True

