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
        new_product = self.product_model(**product_data.model_dump())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        self._create_images(db, new_product.id, image_paths)
        db.commit()

        return new_product
    