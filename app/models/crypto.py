from typing import List
from pydantic import BaseModel, Field


class BaseObjectMetadata(BaseModel):
	id: int = Field(..., description="Id")
	img: str = Field(..., description="Image link")
	area: str = Field(..., description="Area the property located in")
	country: str = Field(..., description="Country the property located in")
	city: str = Field(..., description="City the property located in")
	invested: int = Field(..., description="How much has already invested")
	total: int = Field(..., description="Total amount of NFTs for sale")
	deadline: int = Field(..., description="Timestamp when sale will be closed")
	investors: int = Field(..., description="Current investors amount")


class BriefObjectMetadata(BaseObjectMetadata):
	type: str = Field(..., description="Investment type")
	term: str = Field(..., description="Investment term")
	ltv: float = Field(..., description="LTV")
	annualYield: float = Field(..., description="Annual yield, %")
	totalYield: float = Field(..., description="Cumulative yield, %")


class FullObjectMetadata(BaseObjectMetadata):
	description: str = Field(..., description="Description")
	isActive: bool = Field(..., description="Is the sale active")
	published: int = Field(..., description="Publication date")
	propertyType: str = Field(..., description="Property time")
	propertySize: int = Field(..., description="Property size in ft2 or m2")
	bedrooms: int = Field(..., description="Bedrooms number")
	bathrooms: int = Field(..., description="Bathrooms number")
	title: str = Field(..., description="Title")
	info: str = Field(..., description="Full information")


class ObjectsList(BaseModel):
	objects: List[BriefObjectMetadata] = Field(..., description="List of all available objects")


class NFTMetadata(BaseModel):
	price: float = Field(..., description="NFT price")
	title: str = Field(..., description="NFT title")
