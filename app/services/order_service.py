import datetime
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from decimal import Decimal

from app.enums.order_status_enum import OrderStatusEnum
from app.models.client_model import ClientModel
from app.models.order_item_model import OrderItemModel
from app.models.order_model import OrderModel
from app.models.product_model import ProductModel
from app.schemas.order_schema import OrderCreate, OrderItemCreate, OrderUpdate
from app.services.product_service import ProductService
from app.services.user_service import UserService
from app.utils.db_exceptions import handle_db_exceptions


class OrderService:
    ORDER_NOT_FOUND = "Order not found."
    CANNOT_MODIFY_COMPLETED_ORDER = "Cannot modify a completed order."
    ORDER_ALREADY_CANCELED = "Order is already cancelled."
    ONLY_PAYMENT_OR_CANCELLATION_ALLOWED = "Only payment method or cancellation is allowed for users."
    NO_PERMISSION_TO_DELETE_ORDER = "You do not have permission to delete this order."
    FORBIDDEN_ORDER_ACCESS = "You do not have permission to access this order."

    def __init__(
        self,
        order_model: OrderModel,
        order_items_model: OrderItemModel,
        product_service: ProductService,
        user_service: UserService,
    ):
        self.order_model = order_model
        self.order_items_model = order_items_model
        self.product_service = product_service
        self.user_service = user_service

    @handle_db_exceptions
    def list_orders(
        self,
        db: Session,
        current_user,
        start_date: Optional[datetime.datetime] = None,
        end_date: Optional[datetime.datetime] = None,
        category: Optional[str] = None,
        order_id: Optional[int] = None,
        status: Optional[OrderStatusEnum] = None,
        client_id: Optional[int] = None
    ) -> List[OrderModel]:
        query = db.query(self.order_model)

        filters = []

        if start_date:
            filters.append(self.order_model.created_at >= start_date)
        if end_date:
            filters.append(self.order_model.created_at <= end_date)
        if order_id:
            filters.append(self.order_model.id == order_id)
        if status:
            filters.append(self.order_model.status == status)

        if current_user.role != "ADMIN":
            filters.append(self.order_model.client_id == current_user.id)
        elif client_id:
            filters.append(self.order_model.client_id == client_id)

        if category:
            query = (
                query.join(self.order_model.order_items)
                    .join(self.order_items_model.product)
                    .filter(ProductModel.category.ilike(f"%{category}%"))
            )

        if filters:
            query = query.filter(*filters)

        query = query.options(joinedload(self.order_model.order_items))
        return query.all()

    @handle_db_exceptions
    def create_order(
        self,
        db: Session,
        order_data: OrderCreate,
        current_user: ClientModel
    ) -> OrderModel:
        client = self.user_service.get_user_by_id(
            db, order_data.client_id, current_user
        )

        order_items, total_amount = self._build_order_items(
            db, order_data.order_items
        )

        new_order = self.order_model(
            client_id=client.id,
            status=order_data.status,
            payment_method=order_data.payment_method,
            payment_status=order_data.payment_status,
            total_amount=total_amount,
            created_at=datetime.datetime.now(datetime.timezone.utc)
        )

        db.add(new_order)
        db.flush()

        for item in order_items:
            item.order_id = new_order.id
            db.add(item)

        db.commit()
        db.refresh(new_order)
        return new_order


    def _build_order_items(self, db: Session, items_data: List[OrderItemCreate]):
        order_items = []
        total = Decimal('0.0')

        for item in items_data:
            product = self.product_service.validate_and_decrease_stock(
                db, item.product_id, item.quantity
            )
            price = product.sale_price
            subtotal = price * item.quantity
            total += subtotal

            order_items.append(
                self.order_items_model(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price_at_moment=price
                )
            )

        return order_items, total

    def get_order_by_id(
        self,
        db: Session,
        order_id: int,
        current_user: ClientModel
    ) -> OrderModel:
        order = db.query(self.order_model)\
              .filter(self.order_model.id == order_id).first()
    
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=self.ORDER_NOT_FOUND
            )
        
        if current_user.role != "ADMIN" and order.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=self.FORBIDDEN_ORDER_ACCESS
            )
        
        return order
    
    @handle_db_exceptions
    def update_order(
        self,
        db: Session,
        order_id: int,
        order_data: OrderUpdate,
        current_user
    ) -> OrderModel:
        order = self.get_order_by_id(db, order_id)

        if current_user.role != "ADMIN":
            self._validate_user_modification(order, order_data)
            self._apply_user_changes(db, order, order_data)
        else:
            self._apply_admin_changes(db, order, order_data)

        db.commit()
        db.refresh(order)
        return order

    def _validate_user_modification(self, order, order_data):
        if order.status == OrderStatusEnum.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=self.CANNOT_MODIFY_COMPLETED_ORDER
            )

        if order_data.status == OrderStatusEnum.CANCELED:
            if order.status == OrderStatusEnum.CANCELED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=self.ORDER_ALREADY_CANCELED
                )
        elif order_data.payment_method is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=self.ONLY_PAYMENT_OR_CANCELLATION_ALLOWED
            )

    def _apply_user_changes(self, db, order, order_data):
        if order_data.status == OrderStatusEnum.CANCELED:
            self.product_service.restore_product_stock(db, order)
            order.status = OrderStatusEnum.CANCELED
        elif order_data.payment_method is not None:
            order.payment_method = order_data.payment_method

    def _apply_admin_changes(self, db, order, order_data):
        if order_data.status == OrderStatusEnum.CANCELED and order.status != OrderStatusEnum.CANCELED:
            self.product_service.restore_product_stock(db, order)

        if order_data.status is not None:
            order.status = order_data.status

        if order_data.payment_method is not None:
            order.payment_method = order_data.payment_method

        if order_data.payment_status is not None:
            order.payment_status = order_data.payment_status
    
    @handle_db_exceptions
    def delete_order(self, db: Session, order_id: int, current_user) -> None:
        order = self.get_order_by_id(db, order_id)

        if current_user.role != "ADMIN" and order.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=self.NO_PERMISSION_TO_DELETE_ORDER
            )

        if order.status != OrderStatusEnum.COMPLETED:
            self.product_service.restore_product_stock(db, order)

        for item in order.order_items:
            db.delete(item)

        db.delete(order)
        db.commit()