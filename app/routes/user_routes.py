from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService
from app.database.database import get_db
from app.models.client_model import ClientModel

router = APIRouter(prefix="/api/v1/users", tags=["users"])

def get_user_service() -> UserService:
    return UserService(ClientModel)

@router.get("/", response_model=List[UserResponse], summary="List users")
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    name: Optional[str] = None,
    email: Optional[str] = None,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    return service.list_users(db, skip=skip, limit=limit, name=name, email=email)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Create a user")
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    return service.create_user(db, user_data)

@router.get("/{user_id}", response_model=UserResponse, summary="Get user by ID")
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    return service.get_user_by_id(db, user_id)

@router.put("/{user_id}", response_model=UserResponse, summary="Update user")
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    return service.update_user(db, user_id, user_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete user")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    service.delete_user(db, user_id)
