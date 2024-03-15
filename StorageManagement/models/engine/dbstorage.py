from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker, scoped_session

# mySqlHost = "34.41.208.26"
mySqlHost = "localhost"
mySqlUser = 'root'
# mySqlPass = '\\f.Fe7nG\\Xx\'n"P#'


class DBStorage:
    __engine = None
    __session = None

    def __init__(self, database):
        self.database = database
        self.__engine = create_engine(
            f'mysql+pymysql://{mySqlUser}@{mySqlHost}:3306/{database}',
            pool_size=5,
            pool_recycle=3600,
            pool_pre_ping=True,
            echo=True
        )
        self.reload()
    
    def reload(self):
        if self.database == "User_Management":
            from ..User_Management import Base
        elif self.database == "Content_Management":
            from ..Content_management import Base
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=True)
        session = scoped_session(session_factory)
        self.__session = session()

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def all(self, cls):
        obj_list = []
        for obj in self.__session.scalars(select(cls)).all():
            obj_list.append(obj)
        return obj_list
    
    def search(self, cls, **kwargs):
        obj_list = []
        for obj in self.__session.scalars(select(cls).filter_by(**kwargs)).all():
            obj_list.append(obj)
        if len(obj_list) < 1:
            return None
        return obj_list