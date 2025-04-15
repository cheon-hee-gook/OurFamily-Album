from abc import ABC, abstractmethod
from app.models.user import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    def get_user_by_email(self, email: str) -> User | None: pass

    @abstractmethod
    def create_user(self, email: str, password: str, name: str) -> User: pass
