from fastapi import HTTPException, status
from pytest import Session
from app.models.client_model import ClientModel
from app.schemas.token_schema import TokenSchema
from app.schemas.user_schema import UserCreate
from app.services.jwt_service import JWTService
from app.services.user_service import UserService
import jwt

class AuthService:
    INVALID_CREDENTIALS = "Invalid email or password"
    INVALID_REFRESH_TOKEN = "Invalid refresh token"
    REFRESH_TOKEN_EXPIRED = "Refresh token expired"
    UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED

    def __init__(self, user_service: UserService, jwt_service: JWTService):
        self.user_service = user_service
        self.jwt_service = jwt_service

    def register(self, db: Session, data: UserCreate) -> ClientModel:
        return self.user_service.create_user(db, data)

    def login(self, db:Session, email: str, password: str) -> TokenSchema:
        user = self.user_service.get_user_by_email(db, email)
        if not user or not self.user_service.verify_password(password, user.password):
            raise HTTPException(
                status_code=self.UNAUTHORIZED,
                detail=self.INVALID_CREDENTIALS
            )

        token_data = {"sub": user.email}
        access_token = self.jwt_service.create_access_token(data=token_data)

        return TokenSchema(access_token=access_token)

    def refresh_token(self, refresh_token: str) -> str:
        try:
            payload = self.jwt_service.decode_token(refresh_token)
            email = payload.get("sub")
            if not email:
                raise HTTPException(
                    status_code=self.UNAUTHORIZED,
                    detail=self.INVALID_REFRESH_TOKEN
                )
            return self.jwt_service.create_access_token({"sub": email})
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=self.UNAUTHORIZED,
                detail=self.REFRESH_TOKEN_EXPIRED
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=self.UNAUTHORIZED,
                detail=self.INVALID_REFRESH_TOKEN
            )
