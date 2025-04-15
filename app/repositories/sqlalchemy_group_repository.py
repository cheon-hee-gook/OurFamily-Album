import uuid, random, string
from sqlalchemy.orm import Session
from app.models.group import Group, GroupTypeEnum
from app.models.group_member import GroupMember
from app.repositories.group_repository import GroupRepositoryInterface


class SQLAlchemyGroupRepository(GroupRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def _generate_invite_code(self, length: int = 8):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def create_group(self, name, type, user_id):
        group = Group(
            id=uuid.uuid4(),
            name=name,
            type=GroupTypeEnum(type),
            invite_code=self._generate_invite_code()
        )
        self.db.add(group)
        self.db.flush()

        member = GroupMember(
            id=uuid.uuid4(),
            user_id=user_id,
            group_id=group.id,
            is_admin=True
        )
        self.db.add(member)
        self.db.commit()
        return group

    def join_group(self, user_id, invite_code):
        group = self.db.query(Group).filter(Group.invite_code == invite_code).first()
        if not group:
            raise ValueError("초대 코드에 해당하는 그룹이 없습니다.")
        existing = self.db.query(GroupMember).filter_by(user_id=user_id, group_id=group.id).first()
        if not existing:
            member = GroupMember(id=uuid.uuid4(), user_id=user_id, group_id=group.id)
            self.db.add(member)
            self.db.commit()
        return group

    def get_user_groups(self, user_id):
        return (
            self.db.query(Group)
            .join(GroupMember)
            .filter(GroupMember.user_id == user_id)
            .all()
        )

    def leave_group(self, user_id, group_id):
        member = self.db.query(GroupMember).filter_by(user_id=user_id, group_id=group_id).first()
        if not member:
            raise ValueError("해당 그룹에 가입된 사용자가 아닙니다.")
        self.db.delete(member)
        self.db.commit()
