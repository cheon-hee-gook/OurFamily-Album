import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.models.base import Base


class GroupTypeEnum(str, enum.Enum):
    family = "가족"
    friends = "친구"
    travel = "여행"
    etc = "기타"


class Group(Base):
    __tablename__ = "groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    type = Column(Enum(GroupTypeEnum), default=GroupTypeEnum.family)
    invite_code = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
