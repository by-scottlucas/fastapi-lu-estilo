from pydantic import BaseModel, Field
from typing import Annotated, Optional, List
from decimal import Decimal
from datetime import datetime

from app.enums.order_status_enum import OrderStatusEnum
from app.enums.payment_method_enum import PaymentMethodEnum
from app.enums.payment_status_enum import PaymentStatusEnum
from app.schemas.product_schema import ProductResponse

class OrderItemBase(BaseModel):
    product_id: Optional[int] = Field(
        None,
        title="Product ID",
        description="Unique identifier of the product",
        example=18
    )
    quantity: Annotated[int, Field(gt=0)] = Field(
        None,
        title="Quantity",
        description="Quantity of the product in the order item (must be greater than zero)",
        example=2
    )
    price_at_moment: Optional[Decimal] = Field(
        None,
        title="Price at Moment",
        description="Price of the product at the time of the order",
        example=7500.00
    )

class OrderItemCreate(OrderItemBase):
    product_id: int = Field(
        ...,
        title="Product ID",
        description="Unique identifier of the product",
        example=18
    )
    quantity: Annotated[int, Field(gt=0)] = Field(
        ...,
        title="Quantity",
        description="Quantity of the product in the order item (must be greater than zero)",
        example=2
    )
    price_at_moment: Optional[Decimal] = Field(
        None,
        title="Price at Moment",
        description="Price of the product at the time of the order",
        example=7500.00
    )

class OrderItemResponse(OrderItemBase):
    id: int = Field(
        ...,
        title="Order Item ID",
        description="Unique identifier of the order item",
        example=1
    )
    product: ProductResponse = Field(
        ...,
        title="Product Details",
        description="Complete product information related to this order item"
    )

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    client_id: Optional[int] = Field(
        None,
        title="Client ID",
        description="Unique identifier of the client who made the order",
        example=1
    )
    status: Optional[OrderStatusEnum] = Field(
        None,
        title="Order Status",
        description="Current status of the order",
        example=OrderStatusEnum.PENDING
    )
    payment_method: Optional[PaymentMethodEnum] = Field(
        None,
        title="Payment Method",
        description="Method used to pay the order",
        example=PaymentMethodEnum.BANK_SLIP
    )
    payment_status: Optional[PaymentStatusEnum] = Field(
        None,
        title="Payment Status",
        description="Current payment status of the order",
        example=PaymentStatusEnum.PENDING
    )
    total_amount: Optional[Decimal] = Field(
        None,
        title="Total Amount",
        description="Total amount for the order",
        example=15000.00
    )
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="Datetime when the order was created",
        example="2025-05-25T15:30:00Z"
    )
    order_items: Optional[List[OrderItemResponse]] = Field(
        None,
        title="Products",
        description="List of products/items in the order"
    )

class OrderCreate(OrderBase):
    client_id: int = Field(
        ...,
        title="Client ID",
        description="Unique identifier of the client who made the order",
        example=1
    )
    status: OrderStatusEnum = Field(
        ...,
        title="Order Status",
        description="Current status of the order",
        example=OrderStatusEnum.PENDING
    )
    payment_method: PaymentMethodEnum = Field(
        ...,
        title="Payment Method",
        description="Method used to pay the order",
        example=PaymentMethodEnum.BANK_SLIP
    )
    payment_status: PaymentStatusEnum = Field(
        ...,
        title="Payment Status",
        description="Current payment status of the order",
        example=PaymentStatusEnum.PENDING
    )
    total_amount: Optional[Decimal] = Field(
        None,
        title="Total Amount",
        description="Total amount for the order",
        example=15000.00
    )
    order_items: List[OrderItemCreate] = Field(
        ...,
        title="Products",
        description="List of products/items in the order"
    )

class OrderUpdate(OrderBase):
    status: Optional[OrderStatusEnum] = Field(
        None,
        title="Order Status",
        description="Current status of the order",
        example=OrderStatusEnum.COMPLETED
    )
    payment_status: Optional[PaymentStatusEnum] = Field(
        None,
        title="Payment Status",
        description="Current payment status of the order",
        example=PaymentStatusEnum.PAID
    )

class OrderResponse(OrderBase):
    id: int = Field(
        ...,
        title="Order ID",
        description="Unique identifier of the order",
        example=1
    )
    order_items: List[OrderItemResponse] = Field(
        ...,
        title="Products",
        description="List of products/items in the order"
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "client_id": 1,
                "status": "PENDING",
                "payment_method": "BANK_SLIP",
                "payment_status": "PENDING",
                "total_amount": 15000.00,
                "created_at": "2025-05-25T15:30:00Z",
                "order_items": [
                    {
                        "id": 1,
                        "name": "Apple iPhone 14",
                        "sale_price": 999.99,
                        "description": "Latest model with A15 chip",
                        "stock": 10,
                        "bar_code": "1234567890123",
                        "category": "Smartphones",
                        "expiration_date": "2025-12-31",
                        "images": [
                            {
                                "id": 1,
                                "image_path": "/images/product1.jpg"
                            },
                            {
                                "id": 2,
                                "image_path": "/images/product2.jpg"
                            }
                        ]
                    }
                ]
            }
        }