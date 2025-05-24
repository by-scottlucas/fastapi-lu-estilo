from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.product_image_model import ProductImageModel
from app.models.product_model import ProductModel
from app.schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate
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

@router.get("/{product_id}", response_model=ProductResponse, summary="Get product by ID")
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
    service: ProductService = Depends(get_product_service)
):
    return service.get_product_by_id(db, product_id)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    name: str = Form(...),
    sale_price: float = Form(...),
    description: str = Form(...),
    stock: int = Form(...),
    bar_code: str = Form(...),
    category: str = Form(...),
    images: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    service: ProductService = Depends(get_product_service),
    file_service: FileService = Depends(get_file_service)
):
    product_update = ProductUpdate(
        name=name,
        sale_price=sale_price,
        description=description,
        stock=stock,
        bar_code=bar_code,
        category=category,
    )

    new_image_paths = file_service.save_images(images, category, name)

    updated_product = service.update_product(
        db=db,
        product_id=product_id,
        product_data=product_update,
        new_image_paths=new_image_paths,
        file_service=file_service
    )

    return updated_product

@router.delete("/{product_id}", status_code=204, summary="Delete product")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    service: ProductService = Depends(get_product_service)
):
    service.delete_product(db, product_id)
