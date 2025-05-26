import pytest
from unittest import mock
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from app.models.product_image_model import ProductImageModel
from app.services.product_service import ProductService
from app.models.product_model import ProductModel
from app.schemas.product_schema import ProductCreate, ProductUpdate

@pytest.fixture
def mock_db():
    db_mock = mock.MagicMock(spec=Session)
    db_mock.query.return_value.filter.return_value.first.return_value = None
    return db_mock

@pytest.fixture
def mock_product_image_model():
    return ProductImageModel

@pytest.fixture
def mock_product_model():
    return ProductModel

@pytest.fixture
def product_service(mock_product_model, mock_product_image_model):
    return ProductService(mock_product_model, mock_product_image_model)

@pytest.fixture
def mock_products():
    mock_image_1 = mock.MagicMock(spec=ProductImageModel)
    mock_image_1.id = 1
    mock_image_1.image_path = "/images/summer_floral_dress.jpg"
    mock_image_1.product_id = 1 

    mock_image_2 = mock.MagicMock(spec=ProductImageModel)
    mock_image_2.id = 2
    mock_image_2.image_path = "/images/summer_floral_dress_side.jpg"
    mock_image_2.product_id = 1

    summer_dress = mock.MagicMock(spec=ProductModel)
    summer_dress.id = 1
    summer_dress.name = "Summer Floral Dress"
    summer_dress.sale_price = 129.9
    summer_dress.description = "Light dress with floral print, perfect for warm days."
    summer_dress.stock = 18
    summer_dress.bar_code = "1002003004001"
    summer_dress.category = "Dresses"
    summer_dress.expiration_date = date(2026, 12, 31)
    summer_dress.images = [mock_image_1, mock_image_2]

    winter_coat = mock.MagicMock(spec=ProductModel)
    winter_coat.id = 2
    winter_coat.name = "Winter Coat"
    winter_coat.sale_price = 299.9
    winter_coat.description = "Warm coat for cold winter days."
    winter_coat.stock = 5
    winter_coat.bar_code = "2003004005002"
    winter_coat.category = "Coats"
    winter_coat.expiration_date = date(2027, 1, 31)
    winter_coat.images = []

    return {
        "summer_dress": summer_dress,
        "winter_coat": winter_coat
    }

def test_list_products_with_filters(product_service, mock_db, mock_products):
    query = mock_db.query.return_value
    filtered_query = query.filter.return_value
    paginated_with_offset = filtered_query.offset.return_value
    paginated_with_limit = paginated_with_offset.limit.return_value

    paginated_with_limit.all.return_value = [mock_products["summer_dress"]]

    result = product_service.list_products(
        mock_db,
        skip=0,
        limit=10,
        category="Dresses",
        stock=True,
        min_price=100.0,
        max_price=300.0
    )

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].name == "Summer Floral Dress"

    mock_db.query.assert_called_once_with(product_service.product_model)
    query.filter.assert_called_once()
    filtered_query.offset.assert_called_once_with(0)
    paginated_with_offset.limit.assert_called_once_with(10)
    paginated_with_limit.all.assert_called_once()

def test_get_product_by_id(product_service, mock_db, mock_products):
    product_found = mock_products["summer_dress"]
    
    query_products = mock_db.query.return_value
    query_filtered_by_id = query_products.filter.return_value
    query_filtered_by_id.first.return_value = product_found

    result = product_service.get_product_by_id(mock_db, 1)

    assert result == product_found
    mock_db.query.assert_called_once_with(product_service.product_model)
    query_products.filter.assert_called_once()
    query_filtered_by_id.first.assert_called_once()


def test_create_product_without_images(product_service, mock_db):
    query = mock_db.query.return_value
    filtered_query = query.filter.return_value
    filtered_query.first.return_value = None

    product_data = ProductCreate(
        name="New Product",
        sale_price=50.0,
        description="A new test product",
        stock=10,
        bar_code="1234567890123",
        category="Test Category",
        expiration_date=date(2025, 12, 31),
        images=[]
    )

    with pytest.raises(HTTPException) as exc_info:
        product_service.create_product(mock_db, product_data, image_paths=[])

    assert exc_info.value.status_code == 422 or exc_info.value.status_code == 400
    assert "image" in str(exc_info.value.detail).lower()


def test_create_product_with_images(product_service, mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None

    product_create = ProductCreate(
        name="Product with Images",
        sale_price=70.0,
        description="Product that includes images",
        stock=5,
        bar_code="9876543210987",
        category="Category",
        expiration_date=date(2025, 11, 30),
        images=[]
    )
    image_paths = ["/images/img1.jpg", "/images/img2.jpg"]

    mock_product = mock.MagicMock(spec=ProductModel)
    mock_product.id = 3
    mock_product.name = product_create.name

    def refresh_side_effect(obj):
        if isinstance(obj, ProductModel):
            obj.id = mock_product.id
            obj.name = mock_product.name

    mock_db.refresh.side_effect = refresh_side_effect

    result = product_service.create_product(mock_db, product_create, image_paths)
    
    assert mock_db.add.call_count == 1 + len(image_paths)
    assert mock_db.commit.call_count == 2

    mock_db.refresh.assert_called_once()

    assert result.id == mock_product.id
    assert result.name == product_create.name

    add_calls = mock_db.add.call_args_list
    image_paths_added = [
        call_args[0][0].image_path
        for call_args in add_calls[1:]
        if hasattr(call_args[0][0], "image_path")
    ]
    assert set(image_paths_added) == set(image_paths)

def test_update_product_success(product_service, mock_db, mock_products):
    product_to_update = mock_products["summer_dress"]
    product_to_update.id = 1
    product_to_update.bar_code = "OLD_BARCODE"

    product_service.get_product_by_id = mock.MagicMock(return_value=product_to_update)

    mock_query = mock.MagicMock()
    mock_query.filter.return_value = mock_query 
    mock_query.first.return_value = None        

    mock_db.query.return_value = mock_query

    mock_db.commit = mock.MagicMock()
    mock_db.refresh = mock.MagicMock()

    product_update = ProductUpdate(
        name="Updated Dress",
        sale_price=139.9,
        stock=20,
        bar_code="1002003004009"
    )

    updated_product = product_service.update_product(
        mock_db,
        product_id=product_to_update.id,
        product_data=product_update,
        new_image_paths=None,
        file_service=None
    )

    assert updated_product.name == "Updated Dress"
    assert updated_product.sale_price == 139.9
    assert updated_product.stock == 20
    assert updated_product.bar_code == "1002003004009"
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(product_to_update)
    product_service.get_product_by_id.assert_called_once_with(mock_db, product_to_update.id)

def test_delete_product_success(product_service, mock_db, mock_products):
    product_to_delete = mock_products["summer_dress"]

    product_service.get_product_by_id = mock.MagicMock(return_value=product_to_delete)
    mock_db.delete = mock.MagicMock()
    mock_db.commit = mock.MagicMock()

    with mock.patch('os.path.join', return_value="/mocked/path/to/image.jpg"), \
         mock.patch('os.path.dirname', return_value="/mocked/path/to"), \
         mock.patch('os.path.exists', return_value=True), \
         mock.patch('shutil.rmtree') as mock_rmtree:

        product_service.delete_product(mock_db, product_to_delete.id)

        mock_db.delete.assert_called_once_with(product_to_delete)
        mock_db.commit.assert_called_once()

        mock_rmtree.assert_any_call("/mocked/path/to")
    
    product_service.get_product_by_id.assert_called_once_with(mock_db, product_to_delete.id)


def test_delete_product_not_found(product_service, mock_db):
    product_service.get_product_by_id = mock.MagicMock(
        side_effect=HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=product_service.PRODUCT_NOT_FOUND
        )
    )

    with pytest.raises(HTTPException) as exc:
        product_service.delete_product(mock_db, 999)

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc.value.detail == product_service.PRODUCT_NOT_FOUND
    product_service.get_product_by_id.assert_called_once_with(mock_db, 999)
    mock_db.delete.assert_not_called()
    mock_db.commit.assert_not_called()