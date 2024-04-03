import os

from .engine.dbstorage import DBStorage

environment = os.environ.get("ENV")

print(environment)
if environment == "testing":
    storage1 = DBStorage('test_user_management')
    storage2 = DBStorage('test_content_management')
elif environment == "development":
    storage1 = DBStorage('dev_user_management')
    storage2 = DBStorage('dev_content_management')
elif environment == "production":
    storage1 = DBStorage('user_management')
    storage2 = DBStorage('content_management')

# storage1.reload()
# storage2.reload()
