from fastapi import APIRouter, Depends


from app.models.auth import UserModel
from app.models.crypto import ObjectsList, FullObjectMetadata
from app.helpers.database import db
from app.helpers.crypto import claimDividends
from app.helpers.auth import (
	get_current_user
)

router = APIRouter()


@router.get('/getObject/{object_id}', summary='Get full data for object', response_model=FullObjectMetadata)
async def get_object(object_id: int):
	return db.get_object(object_id)


@router.get('/getObjects', summary='Get list of actual objects', response_model=ObjectsList)
async def get_objects():
	return db.get_objects()


@router.get('/getWalletAddress', summary='Get wallet address of authenticated user', response_model=str)
async def get_wallet_address(user: UserModel = Depends(get_current_user)):
	return user.wallet_address


@router.post('/claimDividends', summary='Initiates a transaction to claim user\'s dividends', response_model=int)
async def claim_dividends(user: UserModel = Depends(get_current_user)):
	return await claimDividends(user.wallet_address)


@router.get('/exportPrivateKey', summary='Export user\'s wallet private key', response_model=str)
async def export_private_key(user: UserModel = Depends(get_current_user)):
	return user.private_key
