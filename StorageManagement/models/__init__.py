import os

from .engine.dbstorage import DBStorage

enviroment = os.environ.get("ENV")

if enviroment == "testing":
    storage1 = DBStorage('test_user_management')
    storage2 = DBStorage('test_content_management')
elif enviroment == "development":
    storage1 = DBStorage('dev_user_management')
    storage2 = DBStorage('dev_content_management')
elif enviroment == "production":
    storage1 = DBStorage('user_management')
    storage2 = DBStorage('content_management')

# storage1.reload()
# storage2.reload()