from faker import Faker

from django.contrib.auth.hashers import make_password

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
