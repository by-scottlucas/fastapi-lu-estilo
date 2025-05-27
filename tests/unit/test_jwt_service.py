import pytest
from fastapi import HTTPException, status
from datetime import timedelta
from app.services.jwt_service import JWTService

def test_create_and_decode_access_token():
    service = JWTService(
        secret_key="test-secret",
        access_token_expire_minutes=1
    )
    data = {"sub": "user123"}
    
    token = service.create_access_token(data)
    decoded = service.decode_token(token)
    
    assert decoded["sub"] == "user123"
    assert "exp" in decoded

def test_create_and_decode_refresh_token():
    service = JWTService(
        secret_key="test-secret",
        refresh_token_expire_days=1
    )
    data = {"sub": "user123"}
    
    token = service.create_refresh_token(data)
    decoded = service.decode_token(token)
    
    assert decoded["sub"] == "user123"
    assert "exp" in decoded

def test_decode_token_expired():
    service = JWTService(secret_key="test-secret")
    data = {"sub": "user123"}
    token = service._build_token(data, timedelta(seconds=-1))
    
    with pytest.raises(HTTPException) as exc:
        service.decode_token(token)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert service.TOKEN_EXPIRED in exc.value.detail

def test_decode_token_invalid():
    service = JWTService(secret_key="test-secret")
    invalid_token = "this.is.an.invalid.token"
    
    with pytest.raises(HTTPException) as exc:
        service.decode_token(invalid_token)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert service.INVALID_TOKEN in exc.value.detail

def test_decode_token_unexpected_error(monkeypatch):
    service = JWTService(secret_key="test-secret")
    data = {"sub": "user123"}
    token = service.create_access_token(data)

    def fake_decode(*args, **kwargs):
        raise Exception("Unexpected error")

    monkeypatch.setattr("jwt.decode", fake_decode)

    with pytest.raises(HTTPException) as exc:
        service.decode_token(token)
    assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert service.UNEXPECTED_ERROR in exc.value.detail