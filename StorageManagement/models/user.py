import os
from sqlalchemy import Column, String, ForeignKey
# from sqlalchemy.orm import relationship
from uuid import uuid4
from werkzeug.utils import secure_filename
# from google.cloud import storage

from .databases.basemodel_1 import Base, BaseModel
from utils.verification import verify_kwargs
from utils.file_manipulation import rand_filename


# # ~~~~~~~ GOOGLE CLOUD STORAGE ~~~~~~~
# try:
#     storage_client = storage.Client()
#     bucket_name = "innovatetogether-hub.appspot.com"
#     bucket = storage_client.bucket(bucket_name)
# except Exception as e:
#     print("Exception occured with google cloud storage library", e)
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
            # # ~~~~~~ SAVE TO GOOGLE CLOUD STORAGE ~~~~~~
            # blob = bucket.blob(f"profile_media/{self.profile_pic_name}")
            # with open("temp/" + self.profile_pic_name, "rb") as file:
            #     blob.upload_from_file(file)
            # # ~~~~~~ SAVE TO GOOGLE CLOUD STORAGE ~~~~~~
            # # ~~~~~~ DELETE FROM TEMPORARY FOLDER ~~~~~~
            # try:
            #     os.remove("temp/" + self.profile_pic_name)
            #     print("File deleted successfully")
            # except PermissionError: 
            #     print("Insufficient permissions to delete file")
            # except FileNotFoundError:
            #     print("File not found")
            # except OSError as error:
            #     print("Error deleting file:", error)
            # # ~~~~~~ DELETE FROM TEMPORARY FOLDER ~~~~~~

            # ~~~~ IMAGE HANDLING ~~~~~~~~~~~

        self.email = kwargs['email']
        self.first_name = kwargs['first_name']
        self.last_name = kwargs['last_name']
        self.password = kwargs['password']