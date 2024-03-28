import os
from uuid import uuid4
from datetime import datetime, timezone

from werkzeug.utils import secure_filename
from sqlalchemy import Column, String, ForeignKey, DATETIME
from sqlalchemy.dialects.mysql import LONGTEXT
# from google.cloud import storage

from .databases.basemodel_2 import Base, BaseModel
from utils.verification import verify_kwargs
from utils.file_manipulation import rand_filename


# storage_client = storage.Client()
# bucket_name = "innovatetogether-hub.appspot.com"
# bucket = storage_client.bucket(bucket_name)


class Post(BaseModel, Base):
    __tablename__ = 'posts'

    user_id = Column(String(150), nullable=False)
    content = Column(LONGTEXT, nullable=False)
    image_url = Column(String(150), nullable=True)
    video_url = Column(String(150), nullable=True)
    send_time = Column(DATETIME, nullable=False, default=datetime.now(timezone.utc))

    def __init__(self, **kwargs):
        verify_kwargs(kwargs, {"user_id"})
        super().__init__()

        # if kwargs.get('image', None) is not None and kwargs["image"].filename != '':
        #     kwargs['image'].filename = secure_filename(kwargs['image'].filename)
        #     self.image_url = rand_filename(kwargs['image'].filename, '.jpg')
        #     kwargs['image'].save(f"temp/{self.image_url}")
        #     # ~~~~~ SAVE TO GOOGLE CLOUD STORAGE ~~~~~
        #     blob = bucket.blob(f"post_media/{self.image_url}")
        #     with open("temp/" + self.image_url, "rb") as file:
        #         blob.upload_from_file(file)
        #     # ~~~~~ SAVE TO GOOGLE CLOUD STORAGE ~~~~~
        #     # ~~~~~ DELETE FROM TEMPORARY FOLDER ~~~~~~
        #     try:
        #         os.remove("temp/" + self.image_url)
        #         print("File deleted successfully")
        #     except PermissionError:
        #         print("Insufficient permissions to delete file")
        #     except FileNotFoundError:
        #         print("File not found")
        #     except OSError as error:
        #         print("Error deleting file:", error)
        #     # ~~~~~ DELETE FROM TEMPORARY FOLDER ~~~~~~

        # if kwargs.get('video', None) is not None and kwargs['video'].filename != '':
        #     kwargs['video'].filename = secure_filename(kwargs['video'].filename)
        #     self.video_url = rand_filename(kwargs['video'].filename, '.mp4')
        #     kwargs['video'].save(f"temp/{self.video_url}")
        #     # ~~~~~ SAVE TO GOOGLE CLOUD STORAGE ~~~~~~
        #     blob = bucket.blob(f"post_media/{self.video_url}")
        #     with open("temp/" + self.video_url, "rb") as file:
        #         blob.upload_from_file(file)
        #     # ~~~~~ SAVE TO GOOGLE CLOUD STORAGE ~~~~~~
        #     # ~~~~~ DELETE FROM TEMPORARY FOLDER ~~~~~~
        #     try:
        #         os.remove("temp/" + self.video_url)
        #         print("File deleted successfully")
        #     except PermissionError:
        #         print("Insufficient permissions to delete file")
        #     except FileNotFoundError:
        #         print("File not found")
        #     except OSError as error:
        #         print("Error deleting file:", error)
        #     # ~~~~~ DELETE FROM TEMPORARY FOLDER ~~~~~~

        self.user_id = kwargs['user_id']
        self.content = kwargs['content']
        self.send_time = datetime.now(timezone.utc)
        