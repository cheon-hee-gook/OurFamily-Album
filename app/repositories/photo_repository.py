from abc import ABC, abstractmethod
from typing import List
from fastapi import UploadFile
from app.models.photo import Photo
from uuid import UUID


class PhotoRepositoryInterface(ABC):
    @abstractmethod
    def get_photo(self, photo_id: UUID) -> Photo | None:
        pass

    @abstractmethod
    def get_group_photos(self, group_id: UUID) -> List[Photo]:
        pass

    @abstractmethod
    def upload_photo(self, uploader_id: UUID, group_id: UUID, file: UploadFile, memo: str, tag_list: list[str]) -> Photo:
        pass

    @abstractmethod
    def delete_photo(self, photo_id: UUID, user_id: UUID) -> None:
        pass
