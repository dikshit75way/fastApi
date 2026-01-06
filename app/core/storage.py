import os
import uuid
import shutil
from fastapi import UploadFile, HTTPException, status

UPLOAD_DIR = "uploads/projects"
IMAGE_UPLOAD_DIR = "uploads/images"
ALLOWED_EXTENSIONS = {".zip"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def save_zip_file(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only ZIP files allowed")

    contents = file.file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = f"{uuid.uuid4()}.zip"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(contents)

    return file_path


def save_image_file(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image files are allowed"
        )

    os.makedirs(IMAGE_UPLOAD_DIR, exist_ok=True)

    filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(IMAGE_UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path
    
    