from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserAuth(BaseModel):
	username: Optional[EmailStr] = Field(description="E-mail")
	password: Optional[str] = Field(min_length=8, max_length=64, description="Password as a plain text")
	wallet_address: Optional[str] = Field(description="EVM blockchain wallet address")
	description: str = Field(..., description="'I am ...' answer from sign up form")
	name: Optional[str] = Field(description="User's name and surname")


class UserModel(BaseModel):
	id: str = Field(..., description="Auto-generated UUID")
	username: Optional[EmailStr] = Field(description="E-mail")
	password: Optional[str] = Field(description="Password as a hash representation")
	wallet_address: Optional[str] = Field(description="EVM blockchain wallet address")
	private_key: Optional[str] = Field(description="Seed phrase for web2 user")
	description: str = Field(..., description="'I am ...' answer from sign up form")
	name: Optional[str] = Field(description="User's name and surname")


class UserLogin(BaseModel):
	username: Optional[EmailStr] = Field(description="E-mail")
	password: Optional[str] = Field(min_length=8, max_length=64, description="Password as a plain text")
	wallet_address: Optional[str] = Field(description="EVM blockchain wallet address")
