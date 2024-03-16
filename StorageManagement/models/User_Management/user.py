from sqlalchemy import Column, String, ForeignKey
# from sqlalchemy.orm import relationship
from uuid import uuid4
import os

from . import Base
from .basemodel import BaseModel
from utils.verification import verify_kwargs


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

        pic_ext = os.path.splitext(kwargs['profile_pic_name'])[1]
        if len(pic_ext) == 0:
            # No file extension added
            pic_ext = '.jpg'
        rand_img_name = f"{uuid4()}{pic_ext}"

        self.profile_pic_name = rand_img_name
        self.email = kwargs['email']
        self.first_name = kwargs['first_name']
        self.last_name = kwargs['last_name']
        self.password = kwargs['password']