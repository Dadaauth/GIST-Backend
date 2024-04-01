from faker import Faker
from threading import Thread
import random
import requests

fake = Faker()

number_of_profiles = 10


# def run_app():
#     # Run application server
#     from main import app
#     import os
#     import sys
#     sys.path.append(os.getcwd())
#     app.run(host="127.0.0.1", port=5000)
#     # Run application server
# thread = Thread(target=run_app)
# thread.start()


images_urls = [
        "https://as2.ftcdn.net/v2/jpg/05/69/94/49/1000_F_569944926_bDeJjYHiLXS8B95a3mNjmoCUKcbaW4rT.jpg",
        "https://as1.ftcdn.net/v2/jpg/05/56/29/10/1000_F_556291020_q2ieMiOCKYbtoLITrnt7qcSL1LJYyWrU.jpg",
        "https://as2.ftcdn.net/v2/jpg/05/50/95/87/1000_F_550958748_OeGcRonEUNoVhd0wjd9zSEMhLFIGO9Bt.jpg",
        "https://as1.ftcdn.net/v2/jpg/00/62/13/24/1000_F_62132429_pw8W4rc1qLlCAP9SS9pPFDZyyPJZHwpw.jpg",
        "https://t4.ftcdn.net/jpg/00/79/19/59/240_F_79195916_9NOsepdkxYHXDZFz9TO4nnsrZ376s0ks.jpg",
        "https://t4.ftcdn.net/jpg/07/61/35/97/240_F_761359772_m77vtLrlLS2I6WDrbvQtmRROerXAVMk8.jpg",
        "https://t4.ftcdn.net/jpg/07/53/23/95/240_F_753239560_OHlLGu92UQ1OftCRmnAli3jtKhgUNl25.jpg",
]
file_names = [
    "one.jpg", "two.jpg", "three.jpg", "four.jpg",
    "five.jpg", "six.jpg", "seven.jpg"
]
# for img_url, name in zip(images_urls, file_names):
#     res = requests.get(img_url)
#     with open(f"temp/{name}", "wb") as f:
#         f.write(res.content)

users = []
image_files_to_close = []

for _ in range(number_of_profiles):
    img_idx = random.randint(0, 6)
    img_f = open(f'temp/{file_names[img_idx]}', "rb")
    image_files_to_close.append(img_f)
    user = {
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "profile_pic": img_f,
        "password": fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
    }
    users.append(user)

with open('./users.csv', "a") as f:
    f.write("EMAIL,PASSWORD\n")
    for user in users:
        f.write(f"{user['email']},{user['password']}\n")

for user in users:
    profile_pic = {"profile_pic": user['profile_pic']}
    del user['profile_pic']
    res = requests.post("http://127.0.0.1:5000/api/v1.0/usermanagement/auth/signup", data=user, files=profile_pic)
    if res.status_code == 201:
        print(f"user [{user['first_name']} {user['last_name']}] has been created...")
    else:
        print("Error creating user", res.status_code, res.text)