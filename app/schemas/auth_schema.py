from pydantic import BaseModel, EmailStr, Field

class LoginSchema(BaseModel):
    email: EmailStr = Field(
        ...,
        title="Email",
        description="User's email address",
        example="john@example.com"
    )
    password: str = Field(
        ...,
        title="Password",
        description="User's password",
        example="strongpassword123"
    )

    class Config:
        schema_extra = {
            "example": {
                "email": "john@example.com",
                "password": "strongpassword123"
            }
        }