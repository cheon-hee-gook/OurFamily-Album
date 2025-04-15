import uuid
from datetime import datetime
from typing import List
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.photo import Photo
from app.models.tag import Tag
from app.models.photo_tag import PhotoTag
from app.repositories.photo_repository import PhotoRepositoryInterface
from app.utils.file_storage import save_file
from uuid import UUID


class SQLAlchemyPhotoRepository(PhotoRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_photo(self, photo_id: UUID) -> Photo | None:
        return self.db.query(Photo).filter(Photo.id == photo_id).first()

    def get_group_photos(self, group_id: UUID) -> List[Photo]:
        return self.db.query(Photo).filter(Photo.group_id == group_id).all()

    def upload_photo(self, uploader_id: UUID, group_id: UUID, file: UploadFile, memo: str, tag_list: list[str]) -> Photo:
        ext = file.filename.rsplit('.', 1)[-1] if '.' in file.filename else 'jpg'
        filename = f"{uuid.uuid4()}.{ext}"
        image_url = save_file(file, filename)

        photo = Photo(
            id=uuid.uuid4(),
            uploader_id=uploader_id,
            group_id=group_id,
            image_url=image_url,
            memo=memo,
            created_at=datetime.utcnow()
        )
        self.db.add(photo)
        self.db.flush()

        for tag_name in tag_list:
            tag = self.db.query(Tag).filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(id=uuid.uuid4(), name=tag_name)
                self.db.add(tag)
                self.db.flush()

            existing = self.db.query(PhotoTag).filter_by(photo_id=photo.id, tag_id=tag.id).first()
            if not existing:
                self.db.add(PhotoTag(id=uuid.uuid4(), photo_id=photo.id, tag_id=tag.id))

        self.db.commit()
        self.db.refresh(photo)
        return photo

    def delete_photo(self, photo_id: UUID, user_id: UUID) -> None:
        photo = self.get_photo(photo_id)
        if not photo:
            raise ValueError("사진이 존재하지 않습니다.")
        if str(photo.uploader_id) != str(user_id):
            raise PermissionError("삭제 권한이 없습니다.")
        self.db.delete(photo)
        self.db.commit()
