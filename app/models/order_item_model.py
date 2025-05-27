from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database.database import Base

class OrderItemModel(Base):
    __tablename__ = "tb_order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("tb_orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("tb_products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price_at_moment = Column(Numeric(10, 2), nullable=False)

    order = relationship("OrderModel", back_populates="order_items")
    product = relationship("ProductModel")