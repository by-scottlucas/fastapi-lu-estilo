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
        example=150.00
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
        example=150.00
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
        example=23
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
        example=350.00
    )
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="Datetime when the order was created",
        example="2025-05-25T15:30:00Z"
    )
    order_items: Optional[List[OrderItemResponse]] = Field(
        None,
        title="Order Items",
        description="List of products/items in the order"
    )

class OrderCreate(OrderBase):
    client_id: int = Field(
        ...,
        title="Client ID",
        description="Unique identifier of the client who made the order",
        example=23
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
        example=350.00
    )
    order_items: List[OrderItemCreate] = Field(
        ...,
        title="Order Items",
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
        example=101
    )
    order_items: List[OrderItemResponse] = Field(
        ...,
        title="Order Items",
        description="List of products/items in the order"
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 101,
                "client_id": 23,
                "status": "PENDING",
                "payment_method": "BANK_SLIP",
                "payment_status": "PENDING",
                "total_amount": 350.00,
                "created_at": "2025-05-25T15:30:00Z",
                "order_items": [
                    {
                        "id": 501,
                        "quantity": 2,
                        "price_at_moment": 50.00,
                        "product": {
                            "id": 1,
                            "name": "Basic Cotton T-Shirt",
                            "sale_price": 50.00,
                            "description": "Basic 100% cotton t-shirt available in various colors",
                            "stock": 120,
                            "bar_code": "7891234567890",
                            "category": "T-Shirts",
                            "expiration_date": None,
                            "images": [
                                {"id": 1, "image_path": "/images/products/basic_cotton_tshirt_1.jpg"},
                                {"id": 2, "image_path": "/images/products/basic_cotton_tshirt_2.jpg"}
                            ]
                        }
                    },
                    {
                        "id": 502,
                        "quantity": 1,
                        "price_at_moment": 150.00,
                        "product": {
                            "id": 2,
                            "name": "Skinny Jeans",
                            "sale_price": 150.00,
                            "description": "Dark wash skinny jeans with stretch fabric",
                            "stock": 75,
                            "bar_code": "7890987654321",
                            "category": "Jeans",
                            "expiration_date": None,
                            "images": [
                                {"id": 3, "image_path": "/images/products/skinny_jeans_1.jpg"}
                            ]
                        }
                    }
                ]
            }
        }
