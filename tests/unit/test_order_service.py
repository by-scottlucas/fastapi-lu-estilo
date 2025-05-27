from decimal import Decimal
import pytest
from unittest.mock import MagicMock

from app.enums.order_status_enum import OrderStatusEnum
from app.models.order_model import OrderModel
from app.models.order_item_model import OrderItemModel
from app.schemas.order_schema import OrderCreate, OrderItemCreate, OrderUpdate
from app.services.order_service import OrderService

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def product_service():
    service = MagicMock()
    service.validate_and_decrease_stock.return_value = MagicMock(sale_price=Decimal('10.00'))
    service.restore_product_stock = MagicMock()
    return service

@pytest.fixture
def user_service():
    service = MagicMock()
    service.get_user_by_id.return_value = MagicMock(id=1)
    return service

@pytest.fixture
def order_service(product_service, user_service):
    return OrderService(
        order_model=OrderModel,
        order_items_model=OrderItemModel,
        product_service=product_service,
        user_service=user_service
    )

@pytest.fixture
def current_user():
    user = MagicMock()
    user.id = 1
    user.role = "USER"
    return user

@pytest.fixture
def admin_user():
    user = MagicMock()
    user.id = 2
    user.role = "ADMIN"
    return user

def test_create_order_success(order_service, mock_db, current_user):
    order_items = [OrderItemCreate(product_id=1, quantity=2)]
    order_data = OrderCreate(
        client_id=1,
        status=OrderStatusEnum.PENDING,
        payment_method="credit_card",
        payment_status="pending",
        order_items=order_items
    )

    mock_db.flush = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    new_order = order_service.create_order(mock_db, order_data, current_user)

    mock_db.add.assert_any_call(new_order)
    mock_db.commit.assert_called_once()

    assert new_order.total_amount == Decimal('20.00')
    assert new_order.status == OrderStatusEnum.PENDING
    assert new_order.payment_method == "credit_card"

def test_build_order_items_calculates_total_and_creates_items(order_service, mock_db):
    items_data = [
        OrderItemCreate(product_id=1, quantity=3),
        OrderItemCreate(product_id=2, quantity=1),
    ]

    def mock_validate_and_decrease_stock(db, product_id, quantity):
        class FakeProduct:
            def __init__(self, price):
                self.sale_price = price

        if product_id == 1:
            return FakeProduct(Decimal('5.00'))
        elif product_id == 2:
            return FakeProduct(Decimal('20.00'))

    order_service.product_service.validate_and_decrease_stock.side_effect = mock_validate_and_decrease_stock

    order_items, total = order_service._build_order_items(mock_db, items_data)

    assert len(order_items) == 2
    assert total == Decimal('35.00')

def test_get_order_by_id_found_and_permission(order_service, mock_db, current_user):
    fake_order = MagicMock()
    fake_order.id = 1
    fake_order.user_id = current_user.id

    query = mock_db.query.return_value
    query.filter.return_value.first.return_value = fake_order

    result = order_service.get_order_by_id(mock_db, 1, current_user)

    assert result == fake_order

def test_get_order_by_id_not_found(order_service, mock_db, current_user):
    query = mock_db.query.return_value
    query.filter.return_value.first.return_value = None

    with pytest.raises(Exception) as exc_info:
        order_service.get_order_by_id(mock_db, 99, current_user)

    assert order_service.ORDER_NOT_FOUND in str(exc_info.value)

def test_update_order_admin_changes(order_service, mock_db, admin_user):
    fake_order = MagicMock()
    fake_order.status = OrderStatusEnum.PENDING

    order_service.get_order_by_id = MagicMock(return_value=fake_order)

    update_data = OrderUpdate(
        status=OrderStatusEnum.CANCELED,
        payment_method="pix",
        payment_status="paid"
    )

    updated_order = order_service.update_order(mock_db, 1, update_data, admin_user)

    order_service.product_service.restore_product_stock.assert_called_once_with(mock_db, fake_order)

    assert updated_order.status == OrderStatusEnum.CANCELED
    assert updated_order.payment_method == "pix"
    assert updated_order.payment_status == "paid"

def test_delete_order_no_permission(order_service, mock_db, current_user):
    fake_order = MagicMock()
    fake_order.client_id = 999
    fake_order.status = OrderStatusEnum.PENDING

    order_service.get_order_by_id = MagicMock(return_value=fake_order)

    with pytest.raises(Exception) as exc_info:
        order_service.delete_order(mock_db, 1, current_user)

    assert order_service.NO_PERMISSION_TO_DELETE_ORDER in str(exc_info.value)

def test_delete_order_success(order_service, mock_db, admin_user):
    fake_order = MagicMock()
    fake_order.client_id = admin_user.id
    fake_order.status = OrderStatusEnum.PENDING
    fake_order.order_items = [MagicMock(), MagicMock()]

    order_service.get_order_by_id = MagicMock(return_value=fake_order)

    order_service.delete_order(mock_db, 1, admin_user)

    order_service.product_service.restore_product_stock.assert_called_once_with(mock_db, fake_order)

    for item in fake_order.order_items:
        mock_db.delete.assert_any_call(item)

    mock_db.delete.assert_any_call(fake_order)
    mock_db.commit.assert_called_once()
