import os

import pytest
from faker import Faker

fake = Faker()
email = fake.email()
first_name = fake.first_name()
last_name = fake.last_name()
password = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)

vars = {}

@pytest.fixture
def setup():
    profile_pic = fake.file_name(extension="jpg")
    profile_tmp_file_url = f"tests/resources/{profile_pic}"
    profile_pic = open(profile_tmp_file_url, "w")
    from StorageManagement.usermanagement import user
    vars['user'] = user
    vars['profile_pic'] = profile_pic
    yield

    profile_pic.close()
    os.remove(profile_tmp_file_url)

def test_create_user(setup):
    user = vars["user"]
    profile_pic = vars['profile_pic']
    # tests the creation of a new user
    with pytest.raises(ValueError):
        user.create_user()
    with pytest.raises(ValueError):
        new_user = user.create_user(email=email, password=password)

    new_user = user.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        profile_pic=profile_pic
    )
    assert new_user[0]
    assert new_user[1].email == email
    assert new_user[1].delete() is None
    assert new_user[1].save() == "D"