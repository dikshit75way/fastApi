import os
import uuid
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = "uploads/projects"
ALLOWED_EXTENSIONS = {".zip"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


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
