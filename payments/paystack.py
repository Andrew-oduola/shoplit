import requests
from django.conf import settings

class Paystack:
    base_url = "https://api.paystack.co"

    def __init__(self):
        self.secret_key = settings.PAYSTACK_SECRET_KEY

    def initialize_payment(self, email, amount):
        url = f"{self.base_url}/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }
        payload = {"email": email, "amount": amount}
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    def verify_payment(self, reference):
        url = f"{self.base_url}/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
        }
        response = requests.get(url, headers=headers)
        return response.json()
