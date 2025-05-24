from typing import Optional, List
from datetime import date
from pydantic import BaseModel

class ProductImageBase(BaseModel):
    image_path: Optional[str] = None

class ProductImageCreate(ProductImageBase):
    image_path: str

class ProductImageResponse(ProductImageBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class ProductBase(BaseModel):
    name: Optional[str] = None
    sale_price: Optional[float] = None
    description: Optional[str] = None
    stock: Optional[int] = None
    bar_code: Optional[str] = None
    category: Optional[str] = None
    expiration_date: Optional[date] = None
    images: Optional[List[ProductImageBase]] = None

class ProductCreate(ProductBase):
    name: str
    sale_price: float
    description: str
    stock: int
    bar_code: str
    category: str

class ProductUpdate(ProductBase):
    pass 

class ProductResponse(ProductBase):
    id: int
    images: List[ProductImageResponse] = []

    model_config = {
        "from_attributes": True
    }
