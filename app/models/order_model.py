from sqlalchemy import Column, Integer, ForeignKey, Enum as SqlEnum, Numeric, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base
from app.enums.order_status_enum import OrderStatusEnum
from app.enums.payment_method_enum import PaymentMethodEnum
from app.enums.payment_status_enum import PaymentStatusEnum

class OrderModel(Base):
    __tablename__ = "tb_orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("tb_clients.id"), nullable=False)
    status = Column(
        SqlEnum(OrderStatusEnum, name="order_status_enum", native_enum=False, validate_strings=True),
        default=OrderStatusEnum.PENDING.value,
        nullable=False
    )
    payment_method = Column(
        SqlEnum(PaymentMethodEnum, name="order_payment_method_enum", native_enum=False, validate_strings=True),
        nullable=True
    )
    payment_status = Column(
        SqlEnum(PaymentStatusEnum, name="payment_status_enum", native_enum=False, validate_strings=True),
        default=PaymentStatusEnum.PENDING.value,
        nullable=False
    )
    total_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    client = relationship("ClientModel")
    order_items = relationship("OrderItemModel", back_populates="order", cascade="all, delete-orphan")
