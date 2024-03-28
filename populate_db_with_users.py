import json
from faker import Faker
import requests
from StorageManagement.usermanagement.user import create_user

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
    res = create_user(
        email=user['email'],
        first_name=user['first_name'],
        last_name=user['last_name'],
        password=user['password'],
    )
    if (res[0]):
        print("User created successfully")
    else:
        print("Error occured when adding new user")
print(json.dumps(users, indent=4))
