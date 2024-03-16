from sqlalchemy import Column, String, ForeignKey
# from sqlalchemy.orm import relationship
from uuid import uuid4
import os

from ..databases.basemodel_1 import Base, BaseModel
from utils.verification import verify_kwargs
from utils.file_manipulation import rand_filename


class User(BaseModel, Base):
    __tablename__ = 'users'

    email = Column(String(200), nullable=False)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    password = Column(String(200), nullable=False)
    profile_pic_name = Column(String(200), nullable=False)

    def __init__(self, **kwargs):
        verify_kwargs(kwargs, {
            "email",
            "first_name",
            "last_name",
            "password",
            "profile_pic_name"
            })
        super().__init__()

        rand_img_name = rand_filename(kwargs['profile_pic_name'], '.jpg')
        self.profile_pic_name = rand_img_name
        self.email = kwargs['email']
        self.first_name = kwargs['first_name']
        self.last_name = kwargs['last_name']
        self.password = kwargs['password']