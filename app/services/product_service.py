import os
import shutil
from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.order_model import OrderModel
from app.models.product_image_model import ProductImageModel
from app.models.product_model import ProductModel
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.services.file_service import FileService
from app.utils.db_exceptions import handle_db_exceptions


class ProductService:
    def __init__(
        self,
        product_model: ProductModel,
        product_image_model: ProductImageModel
    ):
        self.product_model = product_model
        self.product_image_model = product_image_model

    @handle_db_exceptions
    def list_products(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 10,
        stock: Optional[bool] = None,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[ProductModel]:
        query = db.query(self.product_model)
        filters = []

        if stock is not None:
            filters.append(self.product_model.stock > 0 if stock else self.product_model.stock == 0)

        if category:
            filters.append(self.product_model.category.ilike(f"%{category}%"))

        if min_price is not None:
            filters.append(self.product_model.sale_price >= min_price)

        if max_price is not None:
            filters.append(self.product_model.sale_price <= max_price)

        if filters:
            query = query.filter(*filters)

        return query.offset(skip).limit(limit).all()
    
    def _check_bar_code_unique(self, db: Session, bar_code: str, product_id: Optional[int] = None):
        query = db.query(self.product_model).filter(self.product_model.bar_code == bar_code)
        if product_id:
            query = query.filter(self.product_model.id != product_id)
        existing = query.first()
        if existing:
            raise HTTPException(
                status_code=409,
                detail="Bar code already registered."
            )

    @handle_db_exceptions
    def _create_images(self, db: Session, product_id: int, image_paths: List[str]):
        for image_path in image_paths:
            image = self.product_image_model(
                product_id=product_id,
                image_path=image_path
            )
            db.add(image)

    @handle_db_exceptions
    def create_product(
        self,
        db: Session,
        product_data: ProductCreate,
        image_paths: List[str]
    ) -> ProductModel:
        self._check_bar_code_unique(db, product_data.bar_code)

        product_dict = product_data.model_dump()
        product_dict.pop("images", None)

        new_product = self.product_model(**product_dict)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        self._create_images(db, new_product.id, image_paths)
        db.commit()

        return new_product
    
    @handle_db_exceptions
    def get_product_by_id(self, db: Session, product_id: int) -> ProductModel:
        product = db.query(self.product_model).filter(self.product_model.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found."
            )
        return product

    @handle_db_exceptions
    def update_product(
        self,
        db: Session,
        product_id: int,
        product_data: ProductUpdate,
        new_image_paths: Optional[List[str]] = None,
        file_service: Optional[FileService] = None
    ) -> ProductModel:
        product = self.get_product_by_id(db, product_id)

        updated_data = product_data.model_dump(exclude_unset=True)
        new_bar_code = updated_data.get("bar_code")

        if new_bar_code and new_bar_code != product.bar_code:
            self._check_bar_code_unique(db, new_bar_code, product_id=product_id)

        old_product_name = product.name
        old_category_name = product.category

        for field, value in updated_data.items():
            if value is not None:
                setattr(product, field, value)

        new_product_name = product.name
        new_category_name = product.category

        old_folder = file_service._build_product_folder(old_category_name, old_product_name) if file_service else None
        new_folder = file_service._build_product_folder(new_category_name, new_product_name) if file_service else None

        if old_folder and new_folder and old_folder != new_folder:
            if old_folder.exists():
                shutil.rmtree(old_folder)
            new_folder.mkdir(parents=True, exist_ok=True)

        if new_image_paths is not None:
            old_images = db.query(self.product_image_model).filter(
                self.product_image_model.product_id == product.id
            ).all()
            old_image_paths = [img.image_path for img in old_images]

            for img in old_images:
                db.delete(img)
            db.commit()

            if file_service:
                file_service.delete_files(old_image_paths)

            self._create_images(db, product.id, new_image_paths)

        db.commit()
        db.refresh(product)
        return product

    @handle_db_exceptions
    def delete_product(self, db: Session, product_id: int):
        product = self.get_product_by_id(db, product_id)

        for image in product.images:
            full_image_path = os.path.join(os.getcwd(), image.image_path)
            folder_path = os.path.dirname(full_image_path)

            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)

        db.delete(product)
        db.commit()

    @handle_db_exceptions
    def validate_and_decrease_stock(
        self,
        db: Session,
        product_id: int,
        quantity: int
    ) -> ProductModel:
        product = db.query(self.product_model)\
                    .filter(self.product_model.id == product_id)\
                    .with_for_update().first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product not found."
            )

        if product.stock < quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock. Available: {product.stock}"
            )

        product.stock -= quantity
        db.add(product)
        return product
    
    @handle_db_exceptions
    def restore_product_stock(self, db: Session, order: OrderModel):
        for item in order.order_items:
            product = db.query(self.product_model)\
                        .filter(self.product_model.id == item.product_id).first()
            
            if product:
                product.stock += item.quantity
                db.add(product)