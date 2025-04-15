import uuid
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user_repository import UserRepositoryInterface


class SQLAlchemyUserRepository(UserRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, email: str, password: str, name: str) -> User:
        hashed_pw = bcrypt.hash(password)
        user = User(
            id=uuid.uuid4(),
            email=email,
            password_hash=hashed_pw,
            name=name
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
