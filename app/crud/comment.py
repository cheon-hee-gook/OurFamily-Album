import uuid
from sqlalchemy.orm import Session
from app.models.comment import Comment


def add_comment(db: Session, photo_id, author_id, text):
    comment = Comment(
        id=uuid.uuid4(),
        photo_id=photo_id,
        author_id=author_id,
        text=text
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comments(db: Session, photo_id):
    return db.query(Comment).filter(Comment.photo_id == photo_id).all()

