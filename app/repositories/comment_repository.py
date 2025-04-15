from abc import ABC, abstractmethod
from typing import List
from app.models.comment import Comment
from uuid import UUID


class CommentRepositoryInterface(ABC):
    @abstractmethod
    def add_comment(self, photo_id: UUID, author_id: UUID, text: str) -> Comment: pass

    @abstractmethod
    def get_comments(self, photo_id: UUID) -> List[Comment]: pass

    @abstractmethod
    def update_comment(self, comment_id: UUID, user_id: UUID, new_text: str) -> Comment: pass

    @abstractmethod
    def delete_comment(self, comment_id: UUID, user_id: UUID) -> None: pass
