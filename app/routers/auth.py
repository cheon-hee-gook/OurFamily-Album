from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import SignupRequest, LoginRequest, UserResponse, TokenResponse
from app.services import auth_service
from app.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.repositories.user_repository import UserRepositoryInterface
from app.dependencies import get_db
from app.auth_utils import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_user_repository(db: Session = Depends(get_db)) -> UserRepositoryInterface:
    return SQLAlchemyUserRepository(db)


@router.post("/signup", response_model=UserResponse)
def signup(data: SignupRequest,
           repo: UserRepositoryInterface = Depends(get_user_repository)):
    try:
        return auth_service.signup(repo, data.email, data.password, data.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest,
          repo: UserRepositoryInterface = Depends(get_user_repository)):
    try:
        token = auth_service.login(repo, data.email, data.password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user
