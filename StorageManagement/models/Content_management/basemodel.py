from sqlalchemy import Column, Integer, String, DateTime
from uuid import uuid4
from datetime import datetime, timezone

from ..__init__ import storage2


class BaseModel:
    id = Column(String(150), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    def __init__(self):
        self.id = str(uuid4())
        self.created_at = datetime.now(datetime.UTC)
        self.updated_at = datetime.now(datetime.UTC)

    def save(self):
        self.updated_at = datetime.now(timezone.utc)
        storage2.new(self)
        storage2.save()

    @classmethod
    def all(cls):
        """Returns all the instances of the class in storage"""
        return storage1.all(cls)
