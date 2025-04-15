from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentResponse
from app.services import comment_service
from app.repositories.sqlalchemy_comment_repository import SQLAlchemyCommentRepository
from app.repositories.comment_repository import CommentRepositoryInterface
from app.dependencies import get_db
from app.auth_utils import get_current_user

router = APIRouter(prefix="/comments", tags=["Comments"])


def get_comment_repository(db: Session = Depends(get_db)) -> CommentRepositoryInterface:
    return SQLAlchemyCommentRepository(db)


@router.post("/photos/{photo_id}/comments", response_model=CommentResponse)
def create_comment(photo_id: str, data: CommentCreate,
                   repo: CommentRepositoryInterface = Depends(get_comment_repository),
                   current_user: User = Depends(get_current_user)):
    return comment_service.create_comment(repo, photo_id, current_user.id, data.text)


@router.get("/photos/{photo_id}/comments", response_model=list[CommentResponse])
def read_comments(photo_id: str,
                  repo: CommentRepositoryInterface = Depends(get_comment_repository)):
    return comment_service.get_comments(repo, photo_id)


@router.patch("/{comment_id}", response_model=CommentResponse)
def update_comment(comment_id: str, data: CommentCreate,
                   repo: CommentRepositoryInterface = Depends(get_comment_repository),
                   current_user: User = Depends(get_current_user)):
    try:
        return comment_service.update_comment(repo, comment_id, current_user.id, data.text)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{comment_id}")
def delete_comment(comment_id: str,
                   repo: CommentRepositoryInterface = Depends(get_comment_repository),
                   current_user: User = Depends(get_current_user)):
    try:
        comment_service.delete_comment(repo, comment_id, current_user.id)
        return {"message": "댓글 삭제 완료"}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
