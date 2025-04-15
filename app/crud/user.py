from sqlalchemy.orm import Session
from app.models.user import User
import uuid
from passlib.hash import bcrypt


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email: str, password: str, name: str):
    hashed_pw = bcrypt.hash(password)
    user = User(
        id=uuid.uuid4(),
        email=email,
        password_hash=hashed_pw,
        name=name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
