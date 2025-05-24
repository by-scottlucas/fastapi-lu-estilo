from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.product_image_model import ProductImageModel
from app.models.product_model import ProductModel
from app.schemas.product_schema import ProductCreate, ProductResponse
from app.services.product_service import ProductService
from app.services.file_service import FileService
from app.database.database import get_db

router = APIRouter(prefix="/api/v1/products", tags=["products"])

def get_product_service() -> ProductService:
    return ProductService(ProductModel, ProductImageModel)

def get_file_service() -> FileService:
    return FileService()

@router.get("/", response_model=List[ProductResponse], summary="List products")
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    stock: Optional[bool] = None,
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db),
    service: ProductService = Depends(get_product_service)
):
    return service.list_products(
        db,
        skip=skip,
        limit=limit,
        stock=stock,
        category=category,
        max_price=max_price
    )

@router.post("/", response_model=ProductResponse, summary="Create product with images")
def create_product(
    name: str = Form(...),
    sale_price: float = Form(...),
    description: str = Form(...),
    stock: int = Form(...),
    bar_code: str = Form(...),
    category: str = Form(...),
    images: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    service: ProductService = Depends(get_product_service),
    file_service: FileService = Depends(FileService)
):
    image_paths = file_service.save_images(images, category, name)

    product_data = ProductCreate(
        name=name,
        sale_price=sale_price,
        description=description,
        stock=stock,
        bar_code=bar_code,
        category=category
    )

    return service.create_product(db, product_data, image_paths)