from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
	access_token: str = Field(..., description="Access Token")
	refresh_token: str = Field(..., description="Refresh Token")


class TokenPayload(BaseModel):
	username: str = Field(..., description="E-mail")
	expiration: int = Field(..., description="UTC timestamp when token expires")
