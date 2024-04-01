import os
from sqlalchemy import Column, String, ForeignKey
# from sqlalchemy.orm import relationship
from uuid import uuid4
from werkzeug.utils import secure_filename
# from google.cloud import storage

from .databases.basemodel_1 import Base, BaseModel
from utils.verification import verify_kwargs
from utils.file_manipulation import rand_filename


enviroment = os.environ['FLASK_ENV']

# # ~~~~~~~ GOOGLE CLOUD STORAGE ~~~~~~~
try:
    storage_client = storage.Client()
    bucket_name = "innovatetogether-hub.appspot.com"
    bucket = storage_client.bucket(bucket_name)
except Exception as e:
    print("Exception occured with google cloud storage library: ", e)
# # ~~~~~~ GOOGLE CLOUD STORAGE ~~~~~~~



class User(BaseModel, Base):
    __tablename__ = 'users'

    email = Column(String(200), nullable=False)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    password = Column(String(200), nullable=False)
    profile_pic_name = Column(String(200), nullable=True)

    def __init__(self, **kwargs):
        verify_kwargs(kwargs, {
            "email",
            "first_name",
            "last_name",
            "password",
        })
        super().__init__()

        if kwargs['profile_pic']:
            # ~~~~ IMAGE HANDLING ~~~~~~~~~~~
            kwargs['profile_pic'].filename = secure_filename(kwargs['profile_pic'].filename)
            self.profile_pic_name = rand_filename(kwargs['profile_pic'].filename, '.jpg')
            kwargs['profile_pic'].save(f"static/{self.profile_pic_name}")
            # ~~~~~~ SAVE TO GOOGLE CLOUD STORAGE ~~~~~~
            if enviroment == "production":
                try:
                    blob = bucket.blob(f"profile_media/{self.profile_pic_name}")
                    with open("static/" + self.profile_pic_name, "rb") as file:
                        blob.upload_from_file(file)
                    os.remove(f"static/{self.profile_pic_name}")
                    blob.make_public()
                    self.profile_pic_name = blob.public_url
                except Exception as e:
                    print("Could not upload to google cloud: ", e)

            # ~~~~~~ SAVE TO GOOGLE CLOUD STORAGE ~~~~~~
            # ~~~~ IMAGE HANDLING ~~~~~~~~~~~

        self.email = kwargs['email']
        self.first_name = kwargs['first_name']
        self.last_name = kwargs['last_name']
        self.password = kwargs['password']