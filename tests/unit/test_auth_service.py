import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from app.services.auth_service import AuthService
from app.schemas.user_schema import UserCreate
from app.schemas.token_schema import TokenSchema

@pytest.fixture
def user_service_mock():
    return MagicMock()

@pytest.fixture
def jwt_service_mock():
    return MagicMock()

@pytest.fixture
def auth_service(user_service_mock, jwt_service_mock):
    return AuthService(user_service=user_service_mock, jwt_service=jwt_service_mock)

def test_register_calls_create_user(auth_service, user_service_mock):
    db_mock = MagicMock()
    user_data = UserCreate(
        name="John Doe",
        cpf="123.456.789-00",
        email="test@example.com",
        password="123456"
    )

    auth_service.register(db_mock, user_data)
    user_service_mock.create_user.assert_called_once_with(db_mock, user_data)

def test_login_success(auth_service, user_service_mock, jwt_service_mock):
    db_mock = MagicMock()
    email = "test@example.com"
    password = "123456"

    user_mock = MagicMock()
    user_mock.email = email
    user_mock.password = "hashedpassword"

    user_service_mock.get_user_by_email.return_value = user_mock
    user_service_mock.verify_password.return_value = True
    jwt_service_mock.create_access_token.return_value = "token123"

    token = auth_service.login(db_mock, email, password)

    assert isinstance(token, TokenSchema)
    assert token.access_token == "token123"

def test_login_invalid_credentials_raises(auth_service, user_service_mock):
    db_mock = MagicMock()
    email = "test@example.com"
    password = "wrongpassword"

    user_service_mock.get_user_by_email.return_value = None

    with pytest.raises(HTTPException) as exc:
        auth_service.login(db_mock, email, password)

    assert exc.value.status_code == 401
    assert "Invalid email or password" in exc.value.detail

def test_refresh_token_success(auth_service, jwt_service_mock):
    refresh_token = "valid_refresh_token"

    jwt_service_mock.decode_token.return_value = {"sub": "test@example.com"}
    jwt_service_mock.create_access_token.return_value = "new_access_token"

    new_token = auth_service.refresh_token(refresh_token)

    assert new_token == "new_access_token"

def test_refresh_token_expired_raises(auth_service, jwt_service_mock):
    refresh_token = "expired_token"

    from jwt import ExpiredSignatureError
    jwt_service_mock.decode_token.side_effect = ExpiredSignatureError()

    with pytest.raises(HTTPException) as exc:
        auth_service.refresh_token(refresh_token)

    assert exc.value.status_code == 401
    assert "Refresh token expired" in exc.value.detail

def test_refresh_token_invalid_token_raises(auth_service, jwt_service_mock):
    refresh_token = "invalid_token"

    from jwt import InvalidTokenError
    jwt_service_mock.decode_token.side_effect = InvalidTokenError()

    with pytest.raises(HTTPException) as exc:
        auth_service.refresh_token(refresh_token)

    assert exc.value.status_code == 401
    assert "Invalid refresh token" in exc.value.detail

def test_refresh_token_no_email_in_payload_raises(auth_service, jwt_service_mock):
    refresh_token = "token_no_email"

    jwt_service_mock.decode_token.return_value = {}

    with pytest.raises(HTTPException) as exc:
        auth_service.refresh_token(refresh_token)

    assert exc.value.status_code == 401
    assert "Invalid refresh token" in exc.value.detail
