from faker import Faker
from django.conf import settings
from django.contrib.auth.hashers import make_password

import csv
from pprint import pprint

PRODUCTS_METADATA_CSV = settings.DATA_DIR / "ratings_Electronics.csv"

def load_products_data(limit=1):
    with open(PRODUCTS_METADATA_CSV, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        dataset = []
        for i, row in enumerate(reader):
            pprint(row)
            _id = row.get("user_id")
            try:
                _id  = int(_id)
            except:
                _id = None
            data = {
                "user_id": _id,
                "product_id": row.get("product_id"),
                "ratings": row.get("rattings"),
                "timestamp": row.get("timestamp"),
            }
            dataset.append(data)
            if i + 1 >= limit:
                break
            

def get_fake_users(count=10):
    fake = Faker()
    user_data = []
    for _ in range(count):
        user = fake.profile()
        data = {
            "email": user.get("mail"),
            "is_active": True,
            "password": make_password(user.get("mail"))
        }
        if 'name' in user:
            fname, lname = user.get('name').split(" ")[:2]
            data['first_name'] = fname
            data['last_name'] = lname
        user_data.append(data)
    return user_data
