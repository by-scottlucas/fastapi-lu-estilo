from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate
from app.schemas.token_schema import TokenSchema
from app.services.auth_service import AuthService
from app.database.database import get_db

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

auth_service = AuthService()

@router.post("/register", response_model=TokenSchema, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user and return an access token.
    """
    try:
        user = auth_service.register(user_data, db)
        token = auth_service.login(user.email, user.password, db)
        return TokenSchema(access_token=token)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error during registration: {e}"
        )

@router.post("/login", response_model=TokenSchema)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login user with email and password and return access token.
    OAuth2PasswordRequestForm expects 'username' and 'password' fields.
    """
    try:
        token = auth_service.login(form_data.username, form_data.password, db)
        return TokenSchema(access_token=token)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error during login: {e}"
        )

@router.post("/refresh", response_model=TokenSchema)
def refresh_token(refresh_token: str):
    """
    Refresh the access token using a valid refresh token.
    """
    try:
        new_access_token = auth_service.refresh_token(refresh_token)
        return TokenSchema(access_token=new_access_token)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error during token refresh: {e}"
        )
