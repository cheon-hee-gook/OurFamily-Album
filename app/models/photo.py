import uuid
from datetime import datetime
from sqlalchemy import Column, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base


class Photo(Base):
    __tablename__ = "photos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uploader_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id"))
    image_url = Column(Text, nullable=False)
    memo = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    uploader = relationship("User")
    group = relationship("Group")
    tags = relationship(
        "Tag",
        secondary="photo_tags",
        back_populates="photos"
    )
    comments = relationship("Comment", back_populates="photo")