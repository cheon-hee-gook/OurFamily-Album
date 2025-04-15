from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.photo import PhotoResponse
from app.services import photo_service
from app.repositories.sqlalchemy_photo_repository import SQLAlchemyPhotoRepository
from app.repositories.photo_repository import PhotoRepositoryInterface
from app.dependencies import get_db
from app.auth_utils import get_current_user
from app.utils.uuid_utils import to_uuid


router = APIRouter(prefix="/photos", tags=["Photos"])


def get_photo_repository(db: Session = Depends(get_db)) -> PhotoRepositoryInterface:
    return SQLAlchemyPhotoRepository(db)


@router.post("/", response_model=PhotoResponse)
def upload_photo(
    group_id: str = Form(...),
    memo: str = Form(""),
    tags: str = Form(""),
    file: UploadFile = File(...),
    repo: PhotoRepositoryInterface = Depends(get_photo_repository),
    current_user: User = Depends(get_current_user),
):
    tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    try:
        return photo_service.upload_photo(
            repo=repo,
            uploader_id=current_user.id,
            group_id=group_id,
            file=file,
            memo=memo,
            tag_list=tag_list
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[PhotoResponse])
def list_photos(
    group_id: str,
    repo: PhotoRepositoryInterface = Depends(get_photo_repository),
    current_user: User = Depends(get_current_user)
):
    group_id = to_uuid(group_id)
    return repo.get_group_photos(group_id)


@router.get("/{photo_id}", response_model=PhotoResponse)
def get_photo_detail(photo_id: str,
                     repo: PhotoRepositoryInterface = Depends(get_photo_repository),
                     current_user: User = Depends(get_current_user)):
    try:
        return photo_service.get_photo_detail(repo, photo_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{photo_id}")
def delete_photo(photo_id: str,
                 repo: PhotoRepositoryInterface = Depends(get_photo_repository),
                 current_user: User = Depends(get_current_user)):
    try:
        photo_service.delete_photo(repo, photo_id, current_user.id)
        return {"message": "삭제 완료"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
