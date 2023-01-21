from pydantic import BaseModel, Field


class PurchaseModel(BaseModel):
	property_id: int = Field(..., description="Id")
	amount: int = Field(..., description="Number of NFTs user wants to buy")


class PaymentConfirmation(BaseModel):
	merchantAccount: str = Field(..., description="")
	merchantSignature: str = Field(..., description="")
	orderReference: str = Field(..., description="")
	amount: int = Field(..., description="")
	currency: str = Field(..., description="")
	authCode: int = Field(..., description="")
	email: str = Field(..., description="")
	phone: int = Field(..., description="")
	createdDate: int = Field(..., description="")
	processingDate: int = Field(..., description="")
	cardPan: str = Field(..., description="")
	cardType: str = Field(..., description="")
	issuerBankCountry: str = Field(..., description="")
	issuerBankName: str = Field(..., description="")
	transactionStatus: str = Field(..., description="")
	reason: str = Field(..., description="")
	reasonCode: str = Field(..., description="")
	fee: float = Field(..., description="")
	paymentSystem: str = Field(..., description="")
