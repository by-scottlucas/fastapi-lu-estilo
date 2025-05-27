import pytest
from unittest import mock
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.services.user_service import UserService
from app.models.client_model import ClientModel
from app.schemas.user_schema import UserCreate, UserUpdate


@pytest.fixture
def mock_db():
    return mock.MagicMock(spec=Session)

@pytest.fixture
def mock_user_model():
    return ClientModel

@pytest.fixture
def user_service(mock_user_model):
    return UserService(mock_user_model)

@pytest.fixture
def mock_users():
    return {
        "john": ClientModel(id=1, name="John Doe", cpf="123.456.789-00", email="john@example.com", password="strongpassword123", role="user"),
        "jane": ClientModel(id=2, name="Jane Smith", cpf="987.654.321-00", email="jane@example.com", password="securepass456", role="admin"),
        "alice": ClientModel(id=3, name="Alice Wonderland", cpf="111.222.333-44", email="alice@example.com", password="pass123", role="user"),
        "bob": ClientModel(id=4, name="Bob Builder", cpf="555.666.777-88", email="bob@example.com", password="pass456", role="admin")
    }

def test_list_users_with_filters(user_service, mock_db, mock_users):
    query_users = mock_db.query.return_value
    filtered_by_name = query_users.filter.return_value
    filtered_by_email = filtered_by_name.filter.return_value
    paginated_with_offset = filtered_by_email.offset.return_value
    paginated_with_limit = paginated_with_offset.limit.return_value

    paginated_with_limit.all.return_value = [mock_users["john"], mock_users["jane"]]

    result = user_service.list_users(mock_db, name="john", email="john@example.com")

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].name == "John Doe"
    assert result[0].email == "john@example.com"
    assert result[1].name == "Jane Smith"
    assert result[1].email == "jane@example.com"

    mock_db.query.assert_called_once_with(user_service.client_model)
    query_users.filter.assert_called()
    filtered_by_name.filter.assert_called()
    filtered_by_email.offset.assert_called_once_with(0)
    paginated_with_offset.limit.assert_called_once_with(10)
    paginated_with_limit.all.assert_called_once()

def test_list_users_no_filters(user_service, mock_db, mock_users):
    query_users = mock_db.query.return_value
    paginated_with_offset = query_users.offset.return_value
    paginated_with_limit = paginated_with_offset.limit.return_value

    paginated_with_limit.all.return_value = [mock_users["alice"], mock_users["bob"]]

    result = user_service.list_users(mock_db, skip=0, limit=2)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].name == "Alice Wonderland"
    assert result[1].name == "Bob Builder"

    mock_db.query.assert_called_once_with(user_service.client_model)
    query_users.filter.assert_not_called()
    paginated_with_offset.limit.assert_called_once_with(2)
    paginated_with_limit.all.assert_called_once()

def test_list_users_no_results(user_service, mock_db):
    query_users = mock_db.query.return_value
    filtered_by_name = query_users.filter.return_value
    filtered_by_email = filtered_by_name.filter.return_value
    paginated_with_offset = filtered_by_email.offset.return_value
    paginated_with_limit = paginated_with_offset.limit.return_value
    paginated_with_limit.all.return_value = []

    result = user_service.list_users(mock_db, name="nonexistent", email="noone@example.com", skip=10)

    assert isinstance(result, list)
    assert len(result) == 0
    mock_db.query.assert_called_once_with(user_service.client_model)
    query_users.filter.assert_called()
    filtered_by_name.filter.assert_called()
    filtered_by_email.offset.assert_called_once_with(10)
    paginated_with_limit.all.assert_called_once()

def test_create_user(user_service):
    db_mock = mock.MagicMock()

    user_create_data = UserCreate(name="John Doe", cpf="123.456.789-00", email="john@example.com", password="strongpassword123", role="user")

    user_service.get_user_by_cpf = mock.MagicMock(return_value=None)
    user_service.get_user_by_email = mock.MagicMock(return_value=None)

    result = user_service.create_user(db_mock, user_create_data)

    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once()

    assert isinstance(result, ClientModel)
    assert result.name == "John Doe"
    assert result.email == "john@example.com"

def test_create_user_with_existing_email(user_service):
    db_mock = mock.MagicMock()
    user_create_data = UserCreate(name="John Duplicate", cpf="000.000.000-00", email="duplicate@example.com", password="somepass", role="user")

    existing_user_mock = mock.MagicMock()
    user_service.get_user_by_email = mock.MagicMock(return_value=existing_user_mock)
    user_service.get_user_by_cpf = mock.MagicMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        user_service.create_user(db_mock, user_create_data)

    assert exc_info.value.status_code == 409
    assert user_service.EMAIL_ALREADY_REGISTERED in str(exc_info.value.detail)

def test_create_user_with_existing_cpf(user_service):
    db_mock = mock.MagicMock()
    user_create_data = UserCreate(name="Jane Duplicate", cpf="111.222.333-44", email="unique@example.com", password="anotherpass", role="user")

    existing_user_mock = mock.MagicMock()
    user_service.get_user_by_email = mock.MagicMock(return_value=None)
    user_service.get_user_by_cpf = mock.MagicMock(return_value=existing_user_mock)

    with pytest.raises(HTTPException) as exc_info:
        user_service.create_user(db_mock, user_create_data)

    assert exc_info.value.status_code == 409
    assert user_service.CPF_ALREADY_REGISTERED in str(exc_info.value.detail)

def test_get_user_by_id(user_service):
    existing_user_mock = mock.MagicMock()
    user_service.get_user_by_id = mock.MagicMock(return_value=existing_user_mock)
    result = user_service.get_user_by_id(mock.MagicMock(), 1)
    assert result == existing_user_mock

def test_get_user_by_email(user_service):
    existing_user_mock = mock.MagicMock()
    user_service.get_user_by_email = mock.MagicMock(return_value=existing_user_mock)
    result = user_service.get_user_by_email(mock.MagicMock(), "email@example.com")
    assert result == existing_user_mock

def test_get_user_by_cpf(user_service):
    existing_user_mock = mock.MagicMock()
    user_service.get_user_by_cpf = mock.MagicMock(return_value=existing_user_mock)
    result = user_service.get_user_by_cpf(mock.MagicMock(), "123.456.789-00")
    assert result == existing_user_mock

def test_update_user_success(user_service):
    db_mock = mock.MagicMock()
    user_id = 1
    current_user = ClientModel(id=1, role="user")
    user_to_update = mock.MagicMock()
    user_to_update.id = user_id
    user_to_update.password = "old_hashed_password"

    user_service.get_user_by_id = mock.MagicMock(return_value=user_to_update)
    user_service.check_unique_email = mock.MagicMock()
    user_service.check_unique_cpf = mock.MagicMock()
    user_service.hash_password = mock.MagicMock(return_value="new_hashed_password")

    user_data = UserUpdate(email="newemail@example.com", password="newpass")

    updated_user = user_service.update_user(db_mock, user_id, user_data, current_user)

    user_service.check_unique_email.assert_called_once_with(db_mock, "newemail@example.com", exclude_user_id=user_id)
    assert updated_user.password == "new_hashed_password"
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(user_to_update)

def test_update_user_forbidden(user_service):
    db_mock = mock.MagicMock()
    user_id = 2
    current_user = ClientModel(id=1, role="user")
    user_data = UserUpdate(name="New Name")

    with pytest.raises(HTTPException) as exc_info:
        user_service.update_user(db_mock, user_id, user_data, current_user)

    assert exc_info.value.status_code == 403
    assert user_service.ACCESS_DENIED in exc_info.value.detail

def test_update_user_change_role_not_admin(user_service):
    db_mock = mock.MagicMock()
    user_id = 1
    current_user = ClientModel(id=1, role="user")
    user_to_update = mock.MagicMock()
    user_service.get_user_by_id = mock.MagicMock(return_value=user_to_update)
    user_data = UserUpdate(role="admin")

    with pytest.raises(HTTPException) as exc_info:
        user_service.update_user(db_mock, user_id, user_data, current_user)

    assert exc_info.value.status_code == 403
    assert user_service.ADMIN_ROLE_REQUIRED in exc_info.value.detail

def test_update_user_unique_email_and_cpf_check(user_service):
    db_mock = mock.MagicMock()
    user_id = 1
    current_user = ClientModel(id=1, role="admin")
    user_to_update = mock.MagicMock()

    user_service.get_user_by_id = mock.MagicMock(return_value=user_to_update)
    user_service.check_unique_email = mock.MagicMock()
    user_service.check_unique_cpf = mock.MagicMock()
    user_service.hash_password = mock.MagicMock(return_value="hashedpass")

    user_data = UserUpdate(email="admin@example.com", cpf="123.456.789-00", password=None)

    updated_user = user_service.update_user(db_mock, user_id, user_data, current_user)

    user_service.check_unique_email.assert_called_once_with(db_mock, "admin@example.com", exclude_user_id=user_id)
    user_service.check_unique_cpf.assert_called_once_with(db_mock, "123.456.789-00", exclude_user_id=user_id)
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(user_to_update)

def test_delete_user_success(user_service):
    db_mock = mock.MagicMock()
    current_user = ClientModel(id=1, role="admin")
    user_id = 2

    user_service.get_user_by_id = mock.MagicMock(return_value=user_id)

    user_service.delete_user(db_mock, user_id, current_user=current_user)

    db_mock.delete.assert_called_once_with(user_id)
    db_mock.commit.assert_called_once()

def test_delete_user_own_account_forbidden(user_service):
    db_mock = mock.MagicMock()
    current_user = ClientModel(id=1, role="admin")

    with pytest.raises(HTTPException) as exc:
        user_service.delete_user(
            db_mock,
            user_id=current_user.id,
            current_user=current_user
        )
    assert exc.value.status_code == status.HTTP_403_FORBIDDEN
    assert exc.value.detail == user_service.CANNOT_DELETE_OWN_USER

def test_hash_password_and_verify(user_service):
    password = "secret123"
    hashed = user_service.hash_password(password)

    assert hashed != password
    assert user_service.verify_password(password, hashed)
    assert not user_service.verify_password("wrongpassword", hashed)