import uuid
from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.repositories.comment_repository import CommentRepositoryInterface
from uuid import UUID


class SQLAlchemyCommentRepository(CommentRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def add_comment(self, photo_id, author_id, text):
        comment = Comment(id=uuid.uuid4(), photo_id=photo_id, author_id=author_id, text=text)
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_comments(self, photo_id):
        return self.db.query(Comment).filter(Comment.photo_id == photo_id).all()

    def update_comment(self, comment_id, user_id, new_text):
        comment = self.db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise ValueError("댓글이 존재하지 않습니다.")
        if str(comment.author_id) != str(user_id):
            raise PermissionError("댓글 수정 권한이 없습니다.")
        comment.text = new_text
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def delete_comment(self, comment_id, user_id):
        comment = self.db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise ValueError("댓글이 존재하지 않습니다.")
        if str(comment.author_id) != str(user_id):
            raise PermissionError("댓글 삭제 권한이 없습니다.")
        self.db.delete(comment)
        self.db.commit()
