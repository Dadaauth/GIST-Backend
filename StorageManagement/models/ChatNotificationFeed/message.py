from sqlalchemy import Column, String, DATETIME, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import LONGTEXT
from datetime import datetime, timezone

from ..databases.basemodel_2 import Base, BaseModel
from utils.verification import verify_kwargs
from utils.file_manipulation import rand_filename


class Message(BaseModel, Base):
    __tablename__ = 'message'

    sender_id = Column(String(150), nullable=False)
    content = Column(LONGTEXT, nullable=True)
    image_url = Column(String(150), nullable=True)
    video_url = Column(String(150), nullable=True)
    send_time = Column(DATETIME, nullable=False, default=datetime.now(timezone.utc))
    conversation_id = Column(String(150), ForeignKey("conversation.id"), nullable=False)

    def __init__(self, **kwargs):
        verify_kwargs(kwargs, {"sender_id", "conversation_id"})

        super().__init__()

        if kwargs.get('content', None) is not None:
            self.content = kwargs['content']
        if kwargs.get('image_url', None) is not None:
            self.image_url = rand_filename(kwargs['image_url'], '.jpg')
        if kwargs.get('video_url', None) is not None:
            self.video_url = rand_filename(kwargs['video_url'], '.mp4')

        self.sender_id = kwargs['sender_id']
        self.conversation_id = kwargs['conversation_id']
