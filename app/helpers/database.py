import pymongo

from app.core.config import settings
from app.models.auth import UserModel
from app.models.payments import PaymentConfirmation
from app.models.crypto import (
	BriefObjectMetadata,
	FullObjectMetadata,
	ObjectsList,
	NFTMetadata
)


class Database:
	def __init__(self):
		uri = settings.MONGODB_URI.format(settings.MONGODB_USER, settings.MONGODB_PASSWORD)
		self.client = pymongo.MongoClient(uri)
		self.connection = self.client[settings.MONGODB_DATABASE_NAME]

	def get_user(self, username: str = None, wallet_address: str = None) -> UserModel or None:
		result = None

		if username:
			result = self.connection.users.find_one({'username': username})
		elif wallet_address:
			result = self.connection.users.find_one({'wallet_address': wallet_address})

		if result:
			return UserModel.parse_obj(dict(result))
		else:
			return None

	def create_user(self, user: UserModel):
		self.connection.users.insert_one(dict(user))

	def get_object(self, object_id: int):
		return FullObjectMetadata.parse_obj(
			self.connection.objects.find_one({'id': object_id}, {'_id': 0})
		)

	def get_objects(self):
		result = []
		objects = self.connection.objects.find({}, {'_id': 0})

		for _object in list(objects):
			result.append(BriefObjectMetadata.parse_obj(dict(_object)))

		return ObjectsList.parse_obj({'objects': result})

	def get_metadata(self, property_id: int):
		result = self.connection.objects.find_one({'id': property_id}, {'_id': 0})

		if result:
			return NFTMetadata.parse_obj(result)
		else:
			return None

	def get_payment(self, order_reference: str):
		result = self.connection.payments.find_one({
			'orderReference': order_reference
		})

		if result:
			return True
		else:
			return False

	def save_payment(self, data: PaymentConfirmation):
		self.connection.payments.insert_one(data)

	def get_abi(self, name: str):
		result = self.connection.abi.find_one({'name': name}, {'_id': 0})

		return result['abi']


db = Database()
