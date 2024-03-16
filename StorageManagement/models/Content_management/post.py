from uuid import uuid4
import os
from datetime import datetime, timezone

from sqlalchemy import Column, String, ForeignKey, DATETIME
from sqlalchemy.dialects.mysql import LONGTEXT
# from sqlalchemy.orm import relationship

from .import Base
from .basemodel import BaseModel
from utils.verification import verify_kwargs
from utils.file_manipulation import rand_filename


class Post(BaseModel, Base):
    __tablename__ = 'posts'

    user_id = Column(String(150), nullable=False)
    content = Column(LONGTEXT, nullable=False)
    image_url = Column(String(150), nullable=True)
    video_url = Column(String(150), nullable=True)
    send_time = Column(DATETIME, nullable=False, default=datetime.now(timezone.utc))

    def __init__(self, **kwargs):
        verify_kwargs(kwargs, {"user_id", "content"})
        super().__init__()

        if kwargs.get('image_url', None) is not None:
            rand_img_name = rand_filename(kwargs.get('image_url'), '.jpg')
            self.image_url = rand_img_name
        if kwargs.get('video_url', None) is not None:
            rand_video_name = rand_filename(kwargs.get('video_url'), '.mp4')
            self.video_url - rand_video_name
        self.user_id = kwargs['user_id']
        self.content = kwargs['content']
        self.send_time = datetime.now(timezone.utc)
        