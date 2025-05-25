from sqlalchemy import Column, Integer, Numeric, String, Date
from sqlalchemy.orm import relationship
from app.database.database import Base
from app.models.product_image_model import ProductImageModel

class ProductModel(Base):
    __tablename__ = "tb_products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, index=True, nullable=False)
    sale_price = Column(Numeric(10, 2), index=True, nullable=False)
    description = Column(String(120), nullable=False)
    stock = Column(Integer, nullable=False)
    bar_code = Column(String(80), unique=True, nullable=False)
    category = Column(String(50), nullable=False)
    expiration_date = Column(Date, nullable=True)
    images = relationship("ProductImageModel",backref="product",cascade="all, delete-orphan")