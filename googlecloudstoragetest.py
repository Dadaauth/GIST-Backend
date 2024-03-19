from google.cloud import storage

storage_client = storage.Client()

bucket_name = "innovatetogether-hub.appspot.com"
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob("messages_media/clement.jpg")

blob.upload_from_filename("main.py")

# with open("main.py", "r") as f:
#     blob.upload_from_file(f)