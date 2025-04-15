import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base


class PhotoTag(Base):
    __tablename__ = "photo_tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    photo_id = Column(UUID(as_uuid=True), ForeignKey("photos.id"))
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.id"))

    tag = relationship("Tag")