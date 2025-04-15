from app.repositories.comment_repository import CommentRepositoryInterface
from app.models.comment import Comment
from app.utils.uuid_utils import to_uuid


def create_comment(repo: CommentRepositoryInterface, photo_id: str, author_id: str, text: str) -> Comment:
    photo_id = to_uuid(photo_id)
    author_id = to_uuid(author_id)
    return repo.add_comment(photo_id, author_id, text)


def get_comments(repo: CommentRepositoryInterface, photo_id: str):
    photo_id = to_uuid(photo_id)
    return repo.get_comments(photo_id)


def update_comment(repo: CommentRepositoryInterface, comment_id: str, user_id: str, text: str) -> Comment:
    comment_id = to_uuid(comment_id)
    user_id = to_uuid(user_id)
    return repo.update_comment(comment_id, user_id, text)


def delete_comment(repo: CommentRepositoryInterface, comment_id: str, user_id: str):
    comment_id = to_uuid(comment_id)
    user_id = to_uuid(user_id)
    repo.delete_comment(comment_id, user_id)
