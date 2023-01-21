import eth_account

from brownie import Contract, network, web3, accounts

from app.core.config import settings
from app.helpers.database import db


network.connect(settings.WEB3_NETWORK_NAME)
accounts.from_mnemonic(settings.ADMIN_SEED_PHRASE)

manager = eth_account.Account
manager.enable_unaudited_hdwallet_features()

admin = accounts[0]

payment = Contract.from_abi('USDT', settings.PAYMENT_CONTRACT_ADDRESS, db.get_abi('payment'))
phygital = Contract.from_abi('Phygital', settings.PHYGITAL_CONTRACT_ADDRESS, db.get_abi('phygital'))


def validate_address(address: str) -> bool:
	return web3.isAddress(address)


def generate_address() -> [str, str]:
	account, mnemonic = manager.create_with_mnemonic()

	return mnemonic, account.address


def mintItems(buyer, property_id, amount, price):
	tx = payment.increaseAllowance.transact(
		settings.PHYGITAL_CONTRACT_ADDRESS,
		amount * price * 10 ** 6,
		{'from': accounts[0]}
	)

	tx = phygital.mintItems.transact(
		buyer,
		amount,
		property_id,
		{'from': accounts[0]}
	)


async def claimDividends(address) -> bool:
	tx = phygital.claimDividends.transact(
		address,
		{'from': accounts[0]}
	)

	return True
