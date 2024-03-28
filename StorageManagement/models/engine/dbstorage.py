"""DBStorage class module"""
import os

from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError, DatabaseError, DataError


enviroment = os.environ.get("ENV") or "testing"
mySqlHost = os.environ.get('MYSQL_HOST') or "localhost"
mySqlUser = os.environ.get('MYSQL_USER') or "root"
mySqlPassword = os.environ.get('MYSQL_PASSWORD') or "root"

if enviroment == "production":
    mysql_connection_str = f"mysql+pymysql://{mySqlUser}:{mySqlPassword}@{mySqlHost}:3306"
else:
    mysql_connection_str = f"mysql+pymysql://{mySqlUser}@{mySqlHost}:3306"

if enviroment == "testing":
    database1 = 'Test_User_Management'
    database2 = "Test_Content_Management"
elif enviroment == "development":
    database1 = "Dev_User_Management"
    database2 = "Dev_Content_Management"
elif enviroment == "production":
    database1 = "User_Management"
    database2 = "Content_Management"

class DBStorage:
    """DBStorage class:
    
    attributes:
        __engine: engine instance from sqlalchemy
        __session: session object from sqlalchemy


    Method:
        def __init__(self, database):
            initializes the value of self.database.
            inittializes the value of __engine
        def reload(self):
            imports Base from the BaseModel class file.
            Calls Base.metadata.create_all(self.__engine)
            and create a session.
        def new(self, obj):
            adds @obj to the session
        def delete(self, obj):
            deletes an object from the session
        def save(self):
            commits to the database
        def all(self, cls):
            gets all rows in a particular table specified by cls[a class]
        def search(self, cls, **kwargs):
            searches a specific database table using filters specified in kwargs
    """
    __engine = None
    __session = None

    def __init__(self, database):
        """initializes the value of self.database.
            inittializes the value of __engine"""
        self.database = database
        self.__engine = create_engine(
            f'{mysql_connection_str}/{database}',
            pool_size=20,
            pool_recycle=3600,
            pool_pre_ping=True,
            echo=True
        )
        self.reload()
    
    def reload(self):
        """imports Base from the BaseModel class file.
            Calls Base.metadata.create_all(self.__engine)
            and create a session."""
        if self.database == database1:
            from ..databases.basemodel_1 import Base
        elif self.database == database2:
            from ..databases.basemodel_2 import Base
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=True)
        session = scoped_session(session_factory)
        self.__session = session()

    def new(self, obj):
        """adds @obj to the session"""
        self.__session.add(obj)

    def delete(self, obj=None):
        """deletes an object from the session"""
        if obj is not None:
            self.__session.delete(obj)

    def save(self):
        """Commits to the database"""
        try:
            self.__session.commit()
        except (IntegrityError, DatabaseError, DataError) as e:
            print("Error occured during commit: ", e)
            self.__session.rollback()


    def all(self, cls):
        """gets all rows in a particular table specified by cls[a class]"""
        obj_list = []
        for obj in self.__session.scalars(select(cls)).all():
            obj_list.append(obj)
        return obj_list
    
    def search(self, cls, **kwargs):
        """searches a specific database table using filters specified in kwargs"""
        try:
            obj_list = []
            for obj in self.__session.scalars(select(cls).filter_by(**kwargs)).all():
                obj_list.append(obj)
            if len(obj_list) < 1:
                return None
            return obj_list
        except (IntegrityError, DatabaseError, DataError) as e:
            print("Error occured during database search: ", e)
            self.__session.rollback()
            return None