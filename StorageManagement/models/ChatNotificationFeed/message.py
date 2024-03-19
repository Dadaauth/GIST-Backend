from sqlalchemy import Column, String, DATETIME, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import LONGTEXT
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
from google.cloud import storage

from ..databases.basemodel_2 import Base, BaseModel
from utils.verification import verify_kwargs
from utils.file_manipulation import rand_filename

# ~~~~~~~~ GOOGLE CLOUD STORAGE ~~~~~~~~
storage_client = storage.Client()
bucket_name = "innovatetogether-hub.appspot.com"
bucket = storage_client.bucket(bucket_name)
# ~~~~~~~~ GOOGLE CLOUD STORAGE ~~~~~~~~


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


        if kwargs.get('image', None) is not None:
            if kwargs['image'].filename != '':
                kwargs['image'].filename = secure_filename(kwargs['image'].filename)
                self.image_url = rand_filename(kwargs['image'].filename, '.jpg')
                kwargs['image'].save(f"temp/{self.image_url}") # ~~~~ Save to a temporary folder ~~~~
                # ~~~~~~ SAVE TO GOOGLE CLOUD STORAGE ~~~~~~
                blob = bucket.blob(f"messages_media/{self.image_url}")
                blob.upload_from_filename("temp/" + self.image_url)
                # ~~~~~~ SAVE TO GOOGLE CLOUD STORAGE ~~~~~~
        if kwargs.get('video', None) is not None:
            if kwargs['video'].filename != '':
                kwargs['video'].filename = secure_filename(kwargs['video'].filename)
                self.video_url = rand_filename(kwargs['video'].filename, '.mp4')
                kwargs['video'].save(f"temp/{self.video_url}") # ~~~~ Save to a temporary folder ~~~~
                # ~~~~~~ SAVE TO GOOGLE CLOUD STORAGE ~~~~~~
                blob = bucket.blob(f"messages_media/{self.video_url}")
                blob.upload_from_filename("temp/" + self.video_url)
                # ~~~~~~ SAVE TO GOOGLE CLOUD STORAGE ~~~~~~

        self.sender_id = kwargs['sender_id']
        self.conversation_id = kwargs['conversation_id']
