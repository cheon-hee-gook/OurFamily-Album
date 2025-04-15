from pydantic import BaseModel
from uuid import UUID


class TagResponse(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True
