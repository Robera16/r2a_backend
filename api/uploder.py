import firebase_admin
from firebase_admin import credentials, storage
import os
import datetime

bucket = storage.bucket()

def updateFile(media, user_id):
    file_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + str(user_id)
    blob = bucket.blob(file_name)
    blob.upload_from_file(media,content_type=media.content_type)
    blob.make_public()
    return blob.public_url