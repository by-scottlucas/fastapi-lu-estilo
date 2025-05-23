from pydantic import BaseModel

class TokenSchema(BaseModel):
    access_token: str

class RefreshToken(BaseModel):
    refresh_token:str