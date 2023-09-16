import requests

from django.conf import settings


def create_payment(amount: int, currency: str) -> str:
    endpoint = 'https://api.stripe.com/v1/payment_intents'
    headers = {'Authorization': f'Bearer {settings.PAYMENT_SECRET_TOKEN}'}
    data = {
        'amount': amount,
        'currency': currency,
        'payment_method': 'card'
    }

    response = requests.post(endpoint, headers=headers, data=data)
    return response.json()['id']


def make_payment(bill_id: str, number: int, exp_month: int, exp_year: int, cvc: int) -> str:
    endpoint = 'https://api.stripe.com/v1/payment_methods'
    headers = {'Authorization': f'Bearer {settings.PAYMENT_SECRET_TOKEN}'}
    data = {
        'type': 'card',
        'card[number]': number,
        'card[exp_month]': exp_month,
        'card[exp_year]': exp_year,
        'card[cvc]': cvc,

    }

    response = requests.post(endpoint, headers=headers, data=data)
    payment_method_id = response.json()['id']

    endpoint = f'https://api.stripe.com/v1/payment_intents/{bill_id}/confirm'
    headers = {'Authorization': f'Bearer {settings.PAYMENT_SECRET_TOKEN}'}
    data = {
        'payment_method': payment_method_id
    }

    response = requests.post(endpoint, headers=headers, data=data)
    return response.json()['status']


def retrieve_payment(payment_id: str):
    endpoint = f'https://api.stripe.com/v1/payment_intents/{payment_id}'
    headers = {'Authorization': f'Bearer {settings.PAYMENT_SECRET_TOKEN}'}

    response = requests.get(endpoint, headers=headers)
    return response.json()
