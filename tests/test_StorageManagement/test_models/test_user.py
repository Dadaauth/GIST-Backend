import os

import pytest
from faker import Faker

fake = Faker()
email = fake.email()
first_name = fake.first_name()
last_name = fake.last_name()
password = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
profile_pic = fake.file_name(extension="jpg")

@pytest.fixture
def setup():
    yield

def test_user(setup):
    from StorageManagement.usermanagement.user import User
    with pytest.raises(ValueError):
        user = User()
    user = User(email=email,first_name=first_name,last_name=last_name,password=password,profile_pic=profile_pic)
    assert user.email == email
    assert user.first_name == first_name
    assert isinstance(user, User)
    assert user.save() == None
    searched_user = User.search(email=email)[0]
    assert searched_user.email == email
    user.delete()
