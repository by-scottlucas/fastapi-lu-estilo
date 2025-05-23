from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.client_model import ClientModel
from app.schemas.auth_schema import LoginSchema
from app.schemas.user_schema import UserCreate, UserResponse
from app.schemas.token_schema import RefreshToken, TokenSchema
from app.services.auth_service import AuthService
from app.services.jwt_service import JWTService
from app.services.user_service import UserService
from app.database.database import get_db

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

def get_auth_service() -> AuthService:
    jwt_service = JWTService()
    user_service = UserService(client_model=ClientModel)
    return AuthService(user_service=user_service, jwt_service=jwt_service)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        return auth_service.register(db, user_data)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/login", response_model=TokenSchema)
def login(
    login_data: LoginSchema,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        return auth_service.login(db, login_data.email, login_data.password)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/refresh", response_model=TokenSchema)
def refresh_token(
    data: RefreshToken,
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        new_access_token = auth_service.refresh_token(data.refresh_token)
        return TokenSchema(access_token=new_access_token)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )