from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from sqlalchemy.orm import Session

from app.dependencies import admin_required, get_current_user
from app.docs.user_responses import (
    user_not_found_response,
    user_conflict_response,
    internal_server_error_response,
    user_list_responses
)
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService
from app.database.database import get_db
from app.models.client_model import ClientModel

router = APIRouter(prefix="/api/v1/users", tags=["users"])

def get_user_service() -> UserService:
    return UserService(ClientModel)

@router.get(
    "/",
    response_model=List[UserResponse],
    summary="List users",
    description=(
        "Returns a list of all registered users. Only administrators can access this endpoint. "
        "Supports optional filters by name and email, as well as pagination using skip and limit."
    ),
    responses={
        **user_list_responses,
        **internal_server_error_response
    }
)
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    name: Optional[str] = Query(None, description="Filter by user name"),
    email: Optional[str] = Query(None, description="Filter by user email"),
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
    current_user: ClientModel = Depends(admin_required),
):
    return service.list_users(db, skip=skip, limit=limit, name=name, email=email)

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user",
    description=(
        "Creates a new user with the provided information. Only administrators are allowed to perform this operation. "
        "If the email or CPF already exists, a conflict error will be returned."
    ),
    responses={
        **user_conflict_response,
        **internal_server_error_response
    }
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
    current_user: ClientModel = Depends(admin_required),
):
    return service.create_user(db, user_data)

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description=(
        "Returns the details of a user by their ID. Users can only access their own data unless they are administrators."
    ),
    responses={
        **user_not_found_response,
        **internal_server_error_response
    }
)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
    current_user: ClientModel = Depends(get_current_user),
):
    return service.get_user_by_id(db, user_id, current_user)

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    description=(
        "Updates the data of a user by ID. Users can only update their own data unless they are administrators. "
        "Only administrators can update user roles."
    ),
    responses={
        **user_not_found_response,
        **user_conflict_response,
        **internal_server_error_response
    }
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: ClientModel = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    return service.update_user(db, user_id, user_data, current_user)

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description=(
        "Deletes a user by ID. Only administrators can perform this operation. "
        "Administrators are not allowed to delete their own accounts."
    ),
    responses={
        **user_not_found_response,
        **internal_server_error_response
    }
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
    current_user: ClientModel = Depends(admin_required),
):
    service.delete_user(db, user_id, current_user)
