from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.database import Base

class ProductImageModel(Base):
    __tablename__ = "tb_product_images"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String(255), nullable=False)
    product_id = Column(Integer, ForeignKey("tb_products.id", ondelete="CASCADE"))