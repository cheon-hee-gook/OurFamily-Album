from app.repositories.user_repository import UserRepositoryInterface
from app.models.user import User
from passlib.hash import bcrypt
from app.auth_utils import create_access_token


def signup(repo: UserRepositoryInterface, email: str, password: str, name: str) -> User:
    if repo.get_user_by_email(email):
        raise ValueError("이미 등록된 이메일입니다")
    return repo.create_user(email, password, name)


def login(repo: UserRepositoryInterface, email: str, password: str) -> str:
    user = repo.get_user_by_email(email)
    if not user or not bcrypt.verify(password, user.password_hash):
        raise ValueError("이메일 또는 비밀번호가 일치하지 않습니다")
    return create_access_token({ "sub": str(user.id) })
