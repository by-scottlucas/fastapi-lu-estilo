import os
from pathlib import Path
import uuid
import shutil
from typing import List
from fastapi import UploadFile


class FileService:
    def __init__(self):
        upload_path = os.getenv("UPLOAD_PATH")
        if not upload_path:
            raise ValueError("UPLOAD_PATH environment variable is not set")
        
        self.upload_dir = Path(upload_path)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def save_images(
        self,
        images: List[UploadFile],
        category: str,
        product_name: str
    ) -> List[str]:
        product_folder = self.build_product_folder(category, product_name)
        product_folder.mkdir(parents=True, exist_ok=True)

        return [self._save_file(image, product_folder) for image in images]

    def build_product_folder(self, category: str, product_name: str) -> Path:
        safe_category = category.lower().replace(" ", "_")
        safe_name = product_name.lower().replace(" ", "_")
        return self.upload_dir / safe_category / safe_name

    def _save_file(self, image: UploadFile, destination_folder: Path) -> str:
        extension = Path(image.filename).suffix
        unique_name = f"{uuid.uuid4()}{extension}"
        file_path = destination_folder / unique_name

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        return str(file_path)

    def delete_files(self, file_paths: List[str]) -> None:
        for file_path in file_paths:
            try:
                path = Path(file_path)
                if path.exists() and path.is_file():
                    path.unlink()
            except Exception as error:
                print(f"Error deleting file {file_path}: {error}")