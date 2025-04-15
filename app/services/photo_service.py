from app.repositories.photo_repository import PhotoRepositoryInterface
from fastapi import UploadFile
from app.models.photo import Photo
from app.utils.uuid_utils import to_uuid


def upload_photo(repo: PhotoRepositoryInterface, uploader_id: str, group_id: str, file: UploadFile, memo: str, tag_list: list[str]) -> Photo:
    uploader_id = to_uuid(uploader_id)
    group_id = to_uuid(group_id)
    return repo.upload_photo(uploader_id, group_id, file, memo, tag_list)


def get_photo_detail(repo: PhotoRepositoryInterface, photo_id: str) -> Photo:
    photo_id = to_uuid(photo_id)
    photo = repo.get_photo(photo_id)
    if not photo:
        raise ValueError("사진이 존재하지 않습니다.")
    return photo


def delete_photo(repo: PhotoRepositoryInterface, photo_id: str, user_id: str):
    photo_id = to_uuid(photo_id)
    user_id = to_uuid(user_id)
    repo.delete_photo(photo_id, user_id)
