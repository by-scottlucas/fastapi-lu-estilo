import datetime
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from decimal import Decimal

from app.enums.order_status_enum import OrderStatusEnum
from app.models.order_item_model import OrderItemModel
from app.models.order_model import OrderModel
from app.models.product_model import ProductModel
from app.schemas.order_schema import OrderCreate, OrderUpdate
from app.services.product_service import ProductService
from app.utils.db_exceptions import handle_db_exceptions


class OrderService:
    def __init__(
        self,
        order_model: OrderModel,
        order_items_model: OrderItemModel,
        product_service: ProductService
    ):
        self.order_model = order_model
        self.order_items_model = order_items_model
        self.product_service = product_service

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

        if start_date:
            query = query.filter(self.order_model.created_at >= start_date)
        elif end_date:
            query = query.filter(self.order_model.created_at <= end_date)

        if category:
            query = query.join(self.order_model.order_items)\
                .join(self.order_items_model.product)\
                .filter(ProductModel.category.ilike(f"%{category}%"))

        if order_id:
            query = query.filter(self.order_model.id == order_id)

        if status:
            query = query.filter(self.order_model.status == status)

        if current_user.role != "ADMIN":
            query = query.filter(self.order_model.client_id == current_user.id)
        elif client_id: 
            query = query.filter(self.order_model.client_id == client_id)

        query = query.options(joinedload(self.order_model.order_items))
        return query.all()


    @handle_db_exceptions
    def create_order(self, db: Session, order_data: OrderCreate) -> OrderModel:
        total_amount = Decimal('0.0')
        order_item_models = []

        for item in order_data.order_items:
            product = self.product_service.validate_and_decrease_stock(
                db, item.product_id, item.quantity
            )
            price_at_moment = product.sale_price
            subtotal = price_at_moment * item.quantity
            total_amount += subtotal

            order_item = self.order_items_model(
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_moment=price_at_moment
            )
            order_item_models.append(order_item)

        new_order = self.order_model(
            client_id=order_data.client_id,
            status=order_data.status,
            payment_method=order_data.payment_method,
            payment_status=order_data.payment_status,
            total_amount=total_amount,
            created_at=datetime.datetime.now(datetime.timezone.utc)
        )
        db.add(new_order)
        db.flush()

        for order_item in order_item_models:
            order_item.order_id = new_order.id
            db.add(order_item)

        db.commit()
        db.refresh(new_order)

        return new_order
    

    def get_order_by_id(self, db: Session, order_id: int) -> OrderModel:
        order = db.query(self.order_model)\
                  .filter(self.order_model.id == order_id).first()
        
        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found."
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
            if order.status == OrderStatusEnum.COMPLETED:
                raise HTTPException(
                    status_code=400,
                    detail="Cannot modify a completed order."
                )
            
            if order_data.status == OrderStatusEnum.CANCELED:
                if order.status == OrderStatusEnum.CANCELED:
                    raise HTTPException(
                        status_code=400,
                        detail="Order is already cancelled."
                    )
                self.product_service.restore_product_stock(db, order)
                order.status = OrderStatusEnum.CANCELED
            elif order_data.payment_method is not None:
                order.payment_method = order_data.payment_method
            else:
                raise HTTPException(
                    status_code=403,
                    detail="Only payment method or cancellation is allowed for users."
                )
        else:
            if order_data.status == OrderStatusEnum.CANCELED and order.status != OrderStatusEnum.CANCELED:
                self.product_service.restore_product_stock(db, order)
            if order_data.status is not None:
                order.status = order_data.status
            if order_data.payment_method is not None:
                order.payment_method = order_data.payment_method
            if order_data.payment_status is not None:
                order.payment_status = order_data.payment_status

        db.commit()
        db.refresh(order)
        return order
    
    @handle_db_exceptions
    def delete_order(self, db: Session, order_id: int, current_user) -> None:
        order = self.get_order_by_id(db, order_id)

        if current_user.role != "ADMIN" and order.client_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to delete this order."
            )

        if order.status != OrderStatusEnum.COMPLETED:
            self.product_service.restore_product_stock(db, order)

        for item in order.order_items:
            db.delete(item)

        db.delete(order)
        db.commit()