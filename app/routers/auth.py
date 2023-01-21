from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from app.helpers.database import db
from app.models.token import TokenSchema
from app.models.auth import UserAuth, UserModel, UserLogin
from app.helpers.auth import (
	get_hashed_password,
	create_access_token,
	create_refresh_token,
	verify_password,
	validate_refresh_token,
	get_current_user
)
from app.helpers.crypto import (
	validate_address,
	generate_address
)


router = APIRouter()


@router.post('/register', summary="Register Endpoint", tags=["register"], response_model=TokenSchema)
async def register(data: UserAuth):
	user = db.get_user(username=data.username) or db.get_user(wallet_address=data.wallet_address)

	if user:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="User with this email or wallet address already exist"
		)
	else:
		if data.username and data.password:
			private_key, public_key = generate_address()
			user = UserModel.parse_obj({
				'id': str(uuid4()),
				'description': data.description,
				'name': data.name,
				'username': data.username,
				'password': get_hashed_password(data.password),
				'wallet_address': public_key,
				'private_key': private_key
			})
		elif data.wallet_address:
			if validate_address(data.wallet_address):
				user = UserModel.parse_obj({
					'id': str(uuid4()),
					'description': data.description,
					'name': data.name,
					'username': None,
					'password': None,
					'wallet_address': data.wallet_address,
					'private_key': None
				})
			else:
				raise HTTPException(
					status_code=status.HTTP_400_BAD_REQUEST,
					detail="Wallet address is invalid"
				)
		else:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Missing mandatory field"
			)

		db.create_user(user)

		if user.username:
			return {
				"access_token": create_access_token(user.username),
				"refresh_token": create_refresh_token(user.username)
			}
		else:
			return {
				"access_token": "empty",
				"refresh_token": "empty"
			}


@router.post('/login', summary="Login Endpoint", tags=["login"], response_model=TokenSchema)
async def login(data: UserLogin):
	user = db.get_user(username=data.username) or db.get_user(wallet_address=data.wallet_address)

	if not user:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="You have not registered yet"
		)

	else:
		if data.username:
			password = user.password
			if not verify_password(data.password, password):
				raise HTTPException(
					status_code=status.HTTP_400_BAD_REQUEST,
					detail="Incorrect email or password"
				)

			return {
				"access_token": create_access_token(user.username),
				"refresh_token": create_refresh_token(user.username),
			}
		else:
			return {
				"access_token": "empty",
				"refresh_token": "empty"
			}


@router.post('/updateTokens', summary='Get new auth tokens using refresh_token', response_model=TokenSchema)
async def refresh(user: UserModel = Depends(validate_refresh_token)):
	return {
		"access_token": create_access_token(user.username),
		"refresh_token": create_refresh_token(user.username),
	}


@router.get('/me', summary='Get details of current user', response_model=UserModel)
async def get_me(user: UserModel = Depends(get_current_user)):
	return user

