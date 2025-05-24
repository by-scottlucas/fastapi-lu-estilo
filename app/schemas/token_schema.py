from pydantic import BaseModel, Field

class TokenSchema(BaseModel):
    access_token: str = Field(
        ...,
        title="Access Token",
        description="JWT access token for authentication",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )

class RefreshToken(BaseModel):
    refresh_token: str = Field(
        ...,
        title="Refresh Token",
        description="JWT refresh token used to obtain a new access token",
        example="dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4="
    )