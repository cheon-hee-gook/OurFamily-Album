import uuid
import os
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.models.photo import Photo
from app.models.photo_tag import PhotoTag
from app.models.tag import Tag
from app.config.settings import settings
from fastapi import HTTPException


def save_photo_file(upload_file: UploadFile, filename: str) -> str:
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        buffer.write(upload_file.file.read())
    return file_path


def get_group_photos(db: Session, group_id: uuid.UUID):
    return db.query(Photo).filter(Photo.group_id == group_id).all()


def get_photo(db: Session, photo_id: uuid.UUID):
    return db.query(Photo).filter(Photo.id == photo_id).first()


def delete_photo(db: Session, photo_id: str, user_id: str):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise ValueError("사진을 찾을 수 없습니다.")

    if str(photo.uploader_id) != str(user_id):
        raise PermissionError("삭제 권한이 없습니다.")

    db.delete(photo)
    db.commit()
