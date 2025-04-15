from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.group import GroupCreate, GroupResponse
from app.services import group_service
from app.repositories.sqlalchemy_group_repository import SQLAlchemyGroupRepository
from app.repositories.group_repository import GroupRepositoryInterface
from app.dependencies import get_db
from app.auth_utils import get_current_user
from app.models.user import User

router = APIRouter(prefix="/groups", tags=["Groups"])


def get_group_repository(db: Session = Depends(get_db)) -> GroupRepositoryInterface:
    return SQLAlchemyGroupRepository(db)


@router.post("/", response_model=GroupResponse)
def create_group(
    data: GroupCreate,
    repo: GroupRepositoryInterface = Depends(get_group_repository),
    current_user: User = Depends(get_current_user),
):
    return group_service.create_group(repo, data.name, data.type, current_user.id)


@router.post("/join", response_model=GroupResponse)
def join_group(
    invite_code: str,
    repo: GroupRepositoryInterface = Depends(get_group_repository),
    current_user: User = Depends(get_current_user),
):
    try:
        return group_service.join_group(repo, current_user.id, invite_code)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/me", response_model=list[GroupResponse])
def get_my_groups(
    repo: GroupRepositoryInterface = Depends(get_group_repository),
    current_user: User = Depends(get_current_user)
):
    return group_service.get_user_groups(repo, current_user.id)


@router.delete("/{group_id}")
def leave_group(
    group_id: str,
    repo: GroupRepositoryInterface = Depends(get_group_repository),
    current_user: User = Depends(get_current_user)
):
    try:
        group_service.leave_group(repo, current_user.id, group_id)
        return {"message": "그룹에서 탈퇴되었습니다."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
