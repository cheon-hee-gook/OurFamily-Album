from abc import ABC, abstractmethod
from typing import List
from app.models.group import Group
from uuid import UUID


class GroupRepositoryInterface(ABC):
    @abstractmethod
    def create_group(self, name: str, type: str, user_id: UUID) -> Group: pass

    @abstractmethod
    def join_group(self, user_id: UUID, invite_code: str) -> Group: pass

    @abstractmethod
    def get_user_groups(self, user_id: UUID) -> List[Group]: pass

    @abstractmethod
    def leave_group(self, user_id: UUID, group_id: UUID) -> None: pass
