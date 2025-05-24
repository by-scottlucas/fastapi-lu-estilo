import os
from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.product_image_model import ProductImageModel
from app.models.product_model import ProductModel
from app.schemas.product_schema import ProductCreate


class ProductService:
    def __init__(self, product_model: ProductModel, product_image_model: ProductImageModel):
        self.product_model = product_model
        self.product_image_model = product_image_model

    def list_products(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 10,
        stock: Optional[bool] = None,
        category: Optional[str] = None,
        max_price: Optional[float] = None
    ) -> List[ProductModel]:
        query = db.query(self.product_model)
        filters = []

        if stock is not None:
            filters.append(self.product_model.stock > 0 if stock else self.product_model.stock == 0)
        if category:
            filters.append(self.product_model.category.ilike(f"%{category}%"))
        if max_price is not None:
            filters.append(self.product_model.sale_price <= max_price)

        if filters:
            query = query.filter(*filters)

        return query.offset(skip).limit(limit).all()

    def _create_images(self, db: Session, product_id: int, image_paths: List[str]):
        for image_path in image_paths:
            image = self.product_image_model(
                product_id=product_id,
                image_path=image_path
            )
            db.add(image)

    def create_product(
        self,
        db: Session,
        product_data: ProductCreate,
        image_paths: List[str]
    ) -> ProductModel:
        product_dict = product_data.model_dump()
        product_dict.pop("images", None)

        new_product = self.product_model(**product_dict)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        self._create_images(db, new_product.id, image_paths)
        db.commit()

        return new_product
    
    def get_product_by_id(self, db: Session, product_id: int) -> ProductModel:
        product = db.query(self.product_model).filter(self.product_model.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found."
            )
        return product


    def delete_product(self, db: Session, product_id: int):
        product = self.get_product_by_id(product_id)

        project_root = os.getcwd()

        for image in product.images:
            image_full_path = os.path.join(project_root, image.image_path)
            if os.path.exists(image_full_path):
                os.remove(image_full_path)

        db.delete(product)
        db.commit()