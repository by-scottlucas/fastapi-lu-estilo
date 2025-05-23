import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status

INVALID_TOKEN_SUB = "Invalid token: 'sub' claim missing"
TOKEN_EXPIRED = "Token has expired"
INVALID_TOKEN = "Invalid token"
UNEXPECTED_ERROR = "Unexpected error decoding token"

class JWTService:
    def __init__(
        self,
        secret_key: str = os.getenv("SECRET_KEY", "secret-key"),
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 30,
        refresh_token_expire_days: int = 7
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days

    def _build_token(self, data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({
            "exp": expire,
            "sub": str(data.get("sub") or data.get("id"))
        })
        return jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )

    def create_access_token(self, data: dict) -> str:
        return self._build_token(
            data,
            timedelta(minutes=self.access_token_expire_minutes)
        )

    def create_refresh_token(self, data: dict) -> str:
        return self._build_token(
            data,
            timedelta(days=self.refresh_token_expire_days)
        )

    def decode_token(self, token: str) -> str:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=INVALID_TOKEN_SUB
                )
            return username
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=TOKEN_EXPIRED
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INVALID_TOKEN
            )
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{UNEXPECTED_ERROR}: {error}"
            )
