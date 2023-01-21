import hmac
import time
import requests

from app.core.config import settings
from app.helpers.logger import log
from app.helpers.crypto import mintItems
from app.helpers.database import db


def create_invoice(buyer, property_id, price, title, amount) -> str:
    currency = 'USD'
    order_date = int(time.time())
    order_reference = f'{buyer}-{property_id}-{amount}-{int(time.time())}'

    signature_key = f"{settings.WFP_MERCHANT_LOGIN};{settings.WFP_DOMAIN_NAME};" \
                    f"{order_reference};{order_date};" \
                    f"{price * amount};{currency};" \
                    f"{title};{amount};{price}"

    signature = hmac.new(
        settings.WFP_MERCHANT_KEY.encode('utf-8'),
        signature_key.encode('utf-8'),
        digestmod='MD5'
    ).hexdigest()

    result = requests.post(
        settings.WFP_BASE_URL,
        data={
            'merchantAccount': settings.WFP_MERCHANT_LOGIN,
            'merchantDomainName': settings.WFP_DOMAIN_NAME,

            'orderReference': order_reference,
            'orderDate': order_date,

            'amount': price * amount,
            'currency': currency,
            'returnUrl': settings.WFP_PAYMENT_CONFIRMATION_ROUTE,

            'productName': [title],
            'productCount': [amount],
            'productPrice': [price],

            'merchantSignature': str(signature)
        }
    )

    return result.url


def get_last_transactions():
    finish = int(time.time())
    start = finish - 18000

    signature_key = f"{settings.WFP_MERCHANT_LOGIN};{start};{finish}"

    signature = hmac.new(
        settings.WFP_MERCHANT_KEY.encode('utf-8'),
        signature_key.encode('utf-8'),
        digestmod='MD5'
    ).hexdigest()

    result = requests.post(
        settings.WFT_API_BASE_URL,
        json={
            'transactionType': 'TRANSACTION_LIST',
            'merchantAccount': settings.WFP_MERCHANT_LOGIN,
            'merchantSignature': str(signature),
            'apiVersion': 1,
            'dateBegin': start,
            'dateEnd': finish
        }
    )

    if result.status_code == 200 and result.json() and result.json()['reason'] == 'Ok':
        return result.json()['transactionList']
    else:
        return []


def check_payments():
    while True:
        try:
            for transaction in get_last_transactions():
                if transaction['transactionStatus'] == 'Approved':
                    if not db.get_payment(transaction['orderReference']):
                        db.save_payment(transaction)

                        details = transaction['orderReference'].split('-')
                        metadata = db.get_metadata(int(details[1]))

                        mintItems(details[0], int(details[1]), int(details[2]), metadata.price)

            time.sleep(5)

        except Exception as exc:
            log.error(exc)
