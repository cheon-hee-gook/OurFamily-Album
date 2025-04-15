from app.repositories.group_repository import GroupRepositoryInterface
from app.models.group import Group
from typing import List
from app.utils.uuid_utils import to_uuid


def create_group(repo: GroupRepositoryInterface, name: str, type: str, user_id: str) -> Group:
    user_id = to_uuid(user_id)
    return repo.create_group(name, type, user_id)


def join_group(repo: GroupRepositoryInterface, user_id: str, invite_code: str) -> Group:
    user_id = to_uuid(user_id)
    return repo.join_group(user_id, invite_code)


def get_user_groups(repo: GroupRepositoryInterface, user_id: str) -> List[Group]:
    user_id = to_uuid(user_id)
    return repo.get_user_groups(user_id)


def leave_group(repo: GroupRepositoryInterface, user_id: str, group_id: str):
    user_id = to_uuid(user_id)
    group_id = to_uuid(group_id)
    return repo.leave_group(user_id, group_id)
