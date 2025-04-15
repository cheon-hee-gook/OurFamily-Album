import uuid
import random
import string
from sqlalchemy.orm import Session
from app.models.group import Group, GroupTypeEnum
from app.models.group_member import GroupMember


def generate_invite_code(length: int = 8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def create_group(db: Session, name: str, type: str, user_id: uuid.UUID):
    code = generate_invite_code()
    group = Group(
        id=uuid.uuid4(), name=name, type=GroupTypeEnum(type), invite_code=code
    )
    db.add(group)
    db.flush()

    member = GroupMember(
        id=uuid.uuid4(), user_id=user_id, group_id=group.id, is_admin=True
    )
    db.add(member)
    db.commit()
    return group


def get_user_groups(db: Session, user_id: uuid.UUID):
    return (
        db.query(Group)
        .join(GroupMember)
        .filter(GroupMember.user_id == user_id)
        .all()
    )
