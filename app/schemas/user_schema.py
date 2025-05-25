from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from app.enums.role_enum import RoleEnum

class UserBase(BaseModel):
    name: Optional[str] = Field(
        None,
        title="Full name",
        description="User's full name",
        example="John Doe"
    )
    cpf: Optional[str] = Field(
        None,
        title="CPF",
        description="Brazilian individual taxpayer registry identification",
        example="123.456.789-00"
    )
    email: Optional[EmailStr] = Field(
        None,
        title="Email address",
        description="User's email address",
        example="john@example.com"
    )
    password: Optional[str] = Field(
        None,
        title="Password",
        description="User's password",
        example="strongpassword123"
    )
    role: Optional[RoleEnum] = Field(
        RoleEnum.USER,
        title="Role",
        description="User role (user or admin)",
        example="user"
    )

class UserCreate(UserBase):
    name: str = Field(
        ...,
        title="Full name",
        description="User's full name",
        example="John Doe"
    )
    cpf: str = Field(
        ...,
        title="CPF",
        description="Brazilian individual taxpayer registry identification",
        example="123.456.789-00"
    )
    email: EmailStr = Field(
        ...,
        title="Email address",
        description="User's email address",
        example="john@example.com"
    )
    password: str = Field(
        ...,
        title="Password",
        description="User's password",
        example="strongpassword123"
    )
    role: Optional[RoleEnum] = Field(
        RoleEnum.USER,
        title="Role",
        description="User role (user or admin)",
        example="user"
    )


class UserUpdate(UserBase):
    password: Optional[str] = Field(
        None,
        title="Password",
        description="User's password",
        example="newstrongpassword123"
    )

class UserResponse(UserBase):
    id: int = Field(
        ...,
        title="User ID",
        description="Unique identifier for the user",
        example=1
    )
    role: Optional[RoleEnum] = Field(
        RoleEnum.USER,
        title="Role",
        description="User role (user or admin)",
        example="user"
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "cpf": "123.456.789-00",
                "email": "john@example.com",
                "password": "strongpassword123",
                "role": "user"
            }
        }