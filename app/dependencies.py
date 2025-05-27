from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.client_model import ClientModel
from app.enums.role_enum import RoleEnum
from app.services.jwt_service import JWTService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
jwt_service = JWTService()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt_service.decode_token(token)
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except HTTPException:
        raise
    except Exception:
        raise credentials_exception

    user = db.query(ClientModel).filter(ClientModel.email == user_email).first()
    if user is None:
        raise credentials_exception
    return user

def admin_required(
    current_user: ClientModel = Depends(get_current_user),
) -> ClientModel:
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to administrators."
        )
    return current_user
