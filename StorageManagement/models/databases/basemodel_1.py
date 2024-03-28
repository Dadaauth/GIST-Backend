"""BaseModel for the User_Management database"""
import os

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
from uuid import uuid4
from datetime import datetime, timezone

Base = declarative_base()


class BaseModel:
    """BaseModel class for the User_Management database
    
    Atributes:
        id: the id of the new object, automatically assigned in __init__
        created_at: when the object was created.
        updated_at: when the object was created but value is updated when the object is updated

    Methods:
        def __init__(self):
            Initialization method  of the BaseModel class.
            initializes the variables id, created_at, and updated_at.
        def save(self):
            persist the object to database or any other storage
        def delete(self):
            deletes the object from storage or a row from the database.
        def all(cls):
            returns all instances of a particular class in storage.
            This will be all rows in a table when dealing with database storage.
        def search(cls, **kwargs):
            search the storage for a record or list of records based on the dictionary passed to it.
            It only searches based on the class passed to it though.
        def to_dict(self):
            returns a dictionary representation of the object
    """
    id = Column(String(150), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    def __init__(self):
        self.id = str(uuid4())
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
        # print("from basemodel class init method\n\n\n", os.environ.get("ENV"))

    def save(self):
        # print("from basemodel class save method\n\n\n", os.environ.get("ENV"))
        from ..__init__ import storage1
        self.updated_at = datetime.now(timezone.utc)
        storage1.new(self)
        storage1.save()
        storage1.reload()

    def delete(self):
        from ..__init__ import storage1
        storage1.delete(self)
        storage1.save()
        storage1.reload()

    @classmethod
    def all(cls):
        """Returns all the instances of the class in storage"""
        from ..__init__ import storage1
        return storage1.all(cls)
    
    @classmethod
    def search(cls, **kwargs):
        from ..__init__ import storage1
        return storage1.search(cls, **kwargs)
    
    def to_dict(self):
        """Returns a dictionary representation of the model object"""
        dictionary = self.__dict__.copy()
        dictionary.pop('_sa_instance_state', None)
        return dictionary
