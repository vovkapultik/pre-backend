from starlette.routing import RedirectResponse
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import settings
from app.models.auth import UserModel
from app.models.payments import PurchaseModel
from app.helpers.payments import create_invoice
from app.helpers.database import db

from app.helpers.auth import get_current_user


router = APIRouter()


@router.post('/generatePaymentLink', summary='Generate payment link on WFP to purchase NFTs', response_model=str)
async def generate_payment_link(data: PurchaseModel, user: UserModel = Depends(get_current_user)):
	metadata = db.get_metadata(data.property_id)

	if not metadata:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Metadata for this property id not found"
		)

	return create_invoice(
		buyer=user.wallet_address,
		property_id=data.property_id,
		price=metadata.price,
		title=metadata.title,
		amount=data.amount
	)


@router.post('/confirmPayment', summary='Payment confirmation, redirected here from WFP', response_model=bool)
async def confirm_payment():
	return RedirectResponse(
		settings.WFP_DOMAIN_NAME,
		status_code=status.HTTP_302_FOUND
	)
