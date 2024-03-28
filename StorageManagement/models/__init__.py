import os

from .engine.dbstorage import DBStorage

enviroment = os.environ.get("ENV")

if enviroment == "testing":
    storage1 = DBStorage('Test_User_Management')
    storage2 = DBStorage('Test_Content_Management')
elif enviroment == "development":
    storage1 = DBStorage('Dev_User_Management')
    storage2 = DBStorage('Dev_Content_Management')
elif enviroment == "production":
    storage1 = DBStorage('User_Management')
    storage2 = DBStorage('Content_Management')

# storage1.reload()
# storage2.reload()