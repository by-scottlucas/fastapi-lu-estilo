import logging
import pytest
from unittest import mock
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.services.user_service import UserService
from app.models.client_model import ClientModel
from app.schemas.user_schema import UserBase, UserCreate, UserUpdate

@pytest.fixture
def mock_db():
    return mock.MagicMock(spec=Session)

@pytest.fixture
def mock_user_model():
    return ClientModel

@pytest.fixture
def user_service(mock_user_model):
    return UserService(mock_user_model)

def test_list_users_with_filters(user_service, mock_db):
    mock_user_john = ClientModel(
        id=1,
        name="John Doe",
        cpf="123.456.789-00",
        email="john@example.com",
        password="strongpassword123",
        role="user"
    )
    mock_user_jane = ClientModel(
        id=2,
        name="Jane Smith",
        cpf="987.654.321-00",
        email="jane@example.com",
        password="securepass456",
        role="admin"
    )

    query_users = mock_db.query.return_value
    filtered_by_name = query_users.filter.return_value
    filtered_by_email = filtered_by_name.filter.return_value
    paginated_with_offset = filtered_by_email.offset.return_value
    paginated_with_limit = paginated_with_offset.limit.return_value

    paginated_with_limit.all.return_value = [mock_user_john, mock_user_jane]

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


def test_list_users_no_filters(user_service, mock_db):
    mock_user_alice = ClientModel(
        id=3,
        name="Alice Wonderland",
        cpf="111.222.333-44",
        email="alice@example.com",
        password="pass123",
        role="user"
    )
    mock_user_bob = ClientModel(
        id=4,
        name="Bob Builder",
        cpf="555.666.777-88",
        email="bob@example.com",
        password="pass456",
        role="admin"
    )

    query_users = mock_db.query.return_value
    paginated_with_offset = query_users.offset.return_value
    paginated_with_limit = paginated_with_offset.limit.return_value

    paginated_with_limit.all.return_value = [mock_user_alice, mock_user_bob]

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

    result = user_service.list_users(
        mock_db,
        name="nonexistent",
        email="noone@example.com",
        skip=10
    )

    assert isinstance(result, list)
    assert len(result) == 0

    mock_db.query.assert_called_once_with(user_service.client_model)
    query_users.filter.assert_called()
    filtered_by_name.filter.assert_called()
    filtered_by_email.offset.assert_called_once_with(10)
    paginated_with_limit.all.assert_called_once()

def test_create_user(user_service):
    db_mock = mock.MagicMock()

    user_create_data = UserCreate(
        name="John Doe",
        cpf="123.456.789-00",
        email="john@example.com",
        password="strongpassword123",
        role="user"
    )

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

    user_create_data = UserCreate(
        name="John Duplicate",
        cpf="000.000.000-00",
        email="duplicate@example.com",
        password="somepass",
        role="user"
    )

    existing_user_mock = mock.MagicMock()
    user_service.get_user_by_email = mock.MagicMock(return_value=existing_user_mock)
    user_service.get_user_by_cpf = mock.MagicMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        user_service.create_user(db_mock, user_create_data)

    assert exc_info.value.status_code == 409
    assert user_service.EMAIL_ALREADY_REGISTERED in str(exc_info.value.detail)


def test_create_user_with_existing_cpf(user_service):
    db_mock = mock.MagicMock()

    user_create_data = UserCreate(
        name="Jane Duplicate",
        cpf="111.222.333-44",
        email="unique@example.com",
        password="anotherpass",
        role="user"
    )

    existing_user_mock = mock.MagicMock()
    user_service.get_user_by_email = mock.MagicMock(return_value=None)
    user_service.get_user_by_cpf = mock.MagicMock(return_value=existing_user_mock)

    with pytest.raises(HTTPException) as exc_info:
        user_service.create_user(db_mock, user_create_data)

    assert exc_info.value.status_code == 409
    assert user_service.CPF_ALREADY_REGISTERED in str(exc_info.value.detail)