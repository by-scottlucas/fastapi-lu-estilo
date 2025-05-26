import os
import pytest
from unittest import mock
from pathlib import Path
from app.services.file_service import FileService
from fastapi import UploadFile
from io import BytesIO

@pytest.fixture(autouse=True)
def env_upload_path(tmp_path, monkeypatch):
    monkeypatch.setenv("UPLOAD_PATH", str(tmp_path))
    yield

def test_init_creates_upload_dir():
    service = FileService()
    assert service.upload_dir.exists()
    assert service.upload_dir.is_dir()

def test_init_raises_if_no_upload_path(monkeypatch):
    monkeypatch.delenv("UPLOAD_PATH", raising=False)
    with pytest.raises(ValueError):
        FileService()

def test_build_product_folder_returns_correct_path():
    service = FileService()
    path = service.build_product_folder("My Category", "My Product")
    expected = service.upload_dir / "my_category" / "my_product"
    assert path == expected

def test_save_images_creates_folder_and_saves_files(monkeypatch):
    service = FileService()

    monkeypatch.setattr(
        service,
        "_save_file",
        lambda image, folder: f"{folder}/fakefile.jpg"
    )

    images = [mock.MagicMock(spec=UploadFile), mock.MagicMock(spec=UploadFile)]
    category = "Category"
    product_name = "Product"

    saved_paths = service.save_images(images, category, product_name)

    product_folder = service.build_product_folder(category, product_name)
    assert product_folder.exists()
    assert len(saved_paths) == len(images)
    for path in saved_paths:
        assert "fakefile.jpg" in path

def test_save_file_writes_file(tmp_path):
    service = FileService()
    destination_folder = tmp_path

    file_content = b"file content"
    file_like = BytesIO(file_content)
    upload_file = mock.MagicMock(spec=UploadFile)
    upload_file.filename = "test.png"
    upload_file.file = file_like

    saved_path_str = service._save_file(upload_file, destination_folder)
    saved_path = Path(saved_path_str)

    assert saved_path.exists()
    assert saved_path.suffix == ".png"

    with open(saved_path, "rb") as file:
        assert file.read() == file_content