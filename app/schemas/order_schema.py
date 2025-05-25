from pydantic import BaseModel, Field, conint
from typing import Annotated, Optional, List
from decimal import Decimal
from datetime import datetime

from app.enums.order_status_enum import OrderStatusEnum
from app.enums.payment_method_enum import PaymentMethodEnum
from app.enums.payment_status_enum import PaymentStatusEnum

PositiveInt = conint(gt=0)

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
    price_at_moment: Decimal = Field(
        ...,
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

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "product_id": 18,
                "quantity": 2,
                "price_at_moment": 7500.00
            }
        }

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
    products: Optional[List[OrderItemResponse]] = Field(
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
    total_amount: Decimal = Field(
        ...,
        title="Total Amount",
        description="Total amount for the order",
        example=15000.00
    )
    products: List[OrderItemCreate] = Field(
        ...,
        title="Products",
        description="List of products/items in the order"
    )

class OrderUpdate(OrderBase):
    status: Optional[OrderStatusEnum] = Field(
        None,
        title="Order Status",
        description="Current status of the order",
        example=OrderStatusEnum.SHIPPED
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
    products: List[OrderItemResponse] = Field(
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
                "products": [
                    {
                        "id": 1,
                        "product_id": 18,
                        "quantity": 2,
                        "price_at_moment": 7500.00
                    }
                ]
            }
        }