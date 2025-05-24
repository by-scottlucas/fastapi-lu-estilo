from typing import Optional, List
from datetime import date
from pydantic import BaseModel, Field

class ProductImageBase(BaseModel):
    image_path: Optional[str] = Field(
        None,
        title="Image Path",
        description="Path or URL of the product image",
        example="/images/product1.jpg"
    )

class ProductImageCreate(ProductImageBase):
    image_path: str = Field(
        ...,
        title="Image Path",
        description="Path or URL of the product image",
        example="/images/product1.jpg"
    )

class ProductImageResponse(ProductImageBase):
    id: int = Field(
        ...,
        title="Image ID",
        description="Unique identifier of the product image",
        example=1
    )

    model_config = {
        "from_attributes": True
    }

class ProductBase(BaseModel):
    name: Optional[str] = Field(
        None,
        title="Product Name",
        description="Name of the product",
        example="Apple iPhone 14"
    )
    sale_price: Optional[float] = Field(
        None,
        title="Sale Price",
        description="Sale price of the product",
        example=999.99
    )
    description: Optional[str] = Field(
        None,
        title="Description",
        description="Detailed description of the product",
        example="Latest model with A15 chip"
    )
    stock: Optional[int] = Field(
        None,
        title="Stock",
        description="Available stock quantity",
        example=10
    )
    bar_code: Optional[str] = Field(
        None,
        title="Bar Code",
        description="Product bar code",
        example="1234567890123"
    )
    category: Optional[str] = Field(
        None,
        title="Category",
        description="Category of the product",
        example="Smartphones"
    )
    expiration_date: Optional[date] = Field(
        None,
        title="Expiration Date",
        description="Expiration date of the product if applicable",
        example="2025-12-31"
    )
    images: Optional[List[ProductImageBase]] = Field(
        None,
        title="Images",
        description="List of product images"
    )

class ProductCreate(ProductBase):
    name: str = Field(
        ...,
        title="Product Name",
        description="Name of the product",
        example="Apple iPhone 14"
    )
    sale_price: float = Field(
        ...,
        title="Sale Price",
        description="Sale price of the product",
        example=999.99
    )
    description: str = Field(
        ...,
        title="Description",
        description="Detailed description of the product",
        example="Latest model with A15 chip"
    )
    stock: int = Field(
        ...,
        title="Stock",
        description="Available stock quantity",
        example=10
    )
    bar_code: str = Field(
        ...,
        title="Bar Code",
        description="Product bar code",
        example="1234567890123"
    )
    category: str = Field(
        ...,
        title="Category",
        description="Category of the product",
        example="Smartphones"
    )

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int = Field(
        ...,
        title="Product ID",
        description="Unique identifier of the product",
        example=1
    )
    images: List[ProductImageResponse] = Field(
        [],
        title="Images",
        description="List of product images",
        example=[
            {
                "id": 1,
                "image_path": "/images/product1.jpg"
            },
            {
                "id": 2,
                "image_path": "/images/product2.jpg"
            }
        ]
    )

    model_config = {
        "from_attributes": True
    }