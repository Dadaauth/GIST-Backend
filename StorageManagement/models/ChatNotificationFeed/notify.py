from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.mysql import MEDIUMTEXT

from ..databases.basemodel_2 import Base, BaseModel
from utils.verification import verify_kwargs
from utils.file_manipulation import rand_filename


class Notify(Base, BaseModel):
    __tablename__ = "notifications"

    user_id = Column(String(150), nullable=False)
    type = Column(Enum("posts", "friend requests", "calls", "messages"), nullable=False)
    content = Column(MEDIUMTEXT, nullable=False)

    def __init__(self, **kwargs):
        verify_kwargs(kwargs, {"user_id", "type", "content"})
        super().__init__()

        if kwargs['type'] not in {"posts", "friend requests", "calls", "messages"}:
            raise ValueError("post type must be within a certain range. Check database Enum for the ranges...")
        
        self.user_id = kwargs['user_id']
        self.type = kwargs['type']
        self.content = kwargs['content']