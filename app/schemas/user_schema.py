from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserCreate(UserBase):
    name: str
    cpf: str
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }
