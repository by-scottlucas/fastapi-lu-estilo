from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.product_image_model import ProductImageModel
from app.models.product_model import ProductModel
from app.schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService
from app.services.file_service import FileService
from app.database.database import get_db

from app.dependencies import get_current_user, admin_required
from app.models.client_model import ClientModel
from app.docs.product_responses import (
    product_not_found_response,
    product_conflict_response,
    internal_server_error_response,
    product_list_responses
)

router = APIRouter(prefix="/api/v1/products", tags=["products"])

def get_product_service() -> ProductService:
    return ProductService(ProductModel, ProductImageModel)

def get_file_service() -> FileService:
    return FileService()

@router.get(
    "/",
    response_model=List[ProductResponse],
    summary="List products",
    description=(
        "Retrieve a list of products with optional filters:\n\n"
        "- **skip**: number of records to skip (for pagination).\n"
        "- **limit**: maximum number of records to return (default 10, max 100).\n"
        "- **stock**: filter by stock availability. Use `true` to get only products in stock, "
        "`false` for products out of stock, or omit to ignore this filter.\n"
        "- **category**: filter products by exact category name (case-sensitive).\n"
        "- **min_price**: filter products with sale price greater than or equal to this value.\n"
        "- **max_price**: filter products with sale price less than or equal to this value.\n\n"
        "**Example queries:**\n\n"
        "- `/api/v1/products?stock=true&category=Electronics&min_price=500&max_price=1000`\n\n"
        "- `/api/v1/products?skip=20&limit=10`"
    ),
    responses={
        **product_list_responses,
        **internal_server_error_response
    }
)
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    stock: Optional[bool] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db),
    service: ProductService = Depends(get_product_service),
    current_user: ClientModel = Depends(get_current_user),
):
    return service.list_products(
        db,
        skip=skip,
        limit=limit,
        stock=stock,
        category=category,
        min_price=min_price,
        max_price=max_price
    )

@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create product with images",
    description="Create a new product with the given details and upload multiple images.",
    responses={
        **product_conflict_response,
        **internal_server_error_response
    }
)
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
    file_service: FileService = Depends(get_file_service),
    current_user: ClientModel = Depends(admin_required),
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

@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Get product by ID",
    description="Retrieve a product by its unique identifier.",
    responses={
        **product_not_found_response,
        **internal_server_error_response
    }
)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
    service: ProductService = Depends(get_product_service),
    current_user: ClientModel = Depends(get_current_user),
):
    return service.get_product_by_id(db, product_id)

@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update product",
    description="Update an existing product's details and images by its ID.",
    responses={
        **product_not_found_response,
        **product_conflict_response,
        **internal_server_error_response
    }
)
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
    file_service: FileService = Depends(get_file_service),
    current_user: ClientModel = Depends(admin_required),
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

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product",
    description="Delete a product by its ID.",
    responses={
        **product_not_found_response,
        **internal_server_error_response
    }
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    service: ProductService = Depends(get_product_service),
    current_user: ClientModel = Depends(admin_required),
):
    service.delete_product(db, product_id)
