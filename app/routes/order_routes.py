from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies import get_current_user
from app.models.client_model import ClientModel
from app.models.order_item_model import OrderItemModel
from app.models.order_model import OrderModel
from app.models.product_model import ProductModel
from app.schemas.order_schema import OrderCreate, OrderResponse
from app.services.order_service import OrderService
from app.services.product_service import ProductService
from app.enums.order_status_enum import OrderStatusEnum
from app.docs.order_responses import (
    order_not_found_response,
    order_conflict_response,
    order_list_responses,
    internal_server_error_response,
)

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])

def get_order_service() -> OrderService:
    product_service = ProductService(ProductModel, None)
    return OrderService(OrderModel, OrderItemModel, product_service)

@router.get(
    "/",
    response_model=List[OrderResponse],
    summary="Retrieve a list of orders",
    description=(
        "Retrieve orders filtered by optional parameters such as date range, category, "
        "order ID, status, and client ID. If no filter is provided, returns all orders "
        "paginated by default."
    ),
    responses={
        **order_list_responses,
        **order_not_found_response,
        **internal_server_error_response,
    }
)
def list_orders(
    db: Session = Depends(get_db),
    service: OrderService = Depends(get_order_service),
    start_date: Optional[datetime] = Query(
        None, description="Start date (inclusive) to filter orders by their creation date, format: YYYY-MM-DDTHH:MM:SS"
    ),
    end_date: Optional[datetime] = Query(
        None, description="End date (inclusive) to filter orders by their creation date, format: YYYY-MM-DDTHH:MM:SS"
    ),
    category: Optional[str] = Query(
        None, description="Filter orders containing products in this category"
    ),
    order_id: Optional[int] = Query(
        None, description="Filter by specific order ID"
    ),
    status: Optional[OrderStatusEnum] = Query(
        None, description="Filter orders by status (e.g., pending, completed)"
    ),
    client_id: Optional[int] = Query(
        None, description="Filter orders by client ID"
    ),
    current_user: ClientModel = Depends(get_current_user),
):
    return service.list_orders(
        db=db,
        start_date=start_date,
        end_date=end_date,
        category=category,
        order_id=order_id,
        status=status,
        client_id=client_id,
        current_user=current_user
    )

@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new order",
    description=(
        "Create a new order with the provided order details, including items, quantities, "
        "and client information. Returns the created order."
    ),
    responses={
        **order_conflict_response,
        **internal_server_error_response,
    }
)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    service: OrderService = Depends(get_order_service),
    current_user: ClientModel = Depends(get_current_user),
):
    return service.create_order(db, order)
