import json
from faker import Faker
import requests

fake = Faker()

users = []

for _ in range(10):
    user = {
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "profile_pic_name": fake.file_name(extension="jpg"),
        "password": fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
    }
    users.append(user)
for user in users:
    response = requests.post('http://127.0.0.1:5001/api/v1.0/storagemanagement/usermanagement/create_user',
                             json={
                                    "email": user['email'],
                                    "first_name": user["first_name"],
                                    "last_name": user["last_name"],
                                    "profile_pic_name": user["profile_pic_name"],
                                    "password": user["password"]
                                 })
print(response.json())
print(json.dumps(users, indent=4))
