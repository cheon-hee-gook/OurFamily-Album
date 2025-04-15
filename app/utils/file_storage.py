import os
from fastapi import UploadFile
from app.config.settings import settings


def save_file(upload_file: UploadFile, filename: str) -> str:
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    path = os.path.join(settings.UPLOAD_DIR, filename)
    with open(path, "wb") as buffer:
        buffer.write(upload_file.file.read())
    return path
