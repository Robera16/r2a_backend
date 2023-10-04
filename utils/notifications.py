import requests
from firebase_admin import firestore
import os
db = firestore.client()
notification_url = os.environ['FIREBASE_MESSAGE_URL']
import json

def send_push_notification(from_user, to_user, notification_dict):
    user = db.collection(u'users').where(u'r2aId', u'==', to_user.id).limit(1).get()
    if(len(user) > 0):
        token = user[0].to_dict().get("pushToken")
        # add recepeints token here
        notification_dict['to'] = token
        request_dict = json.dumps(notification_dict)
        try:
            resp = requests.post(notification_url, request_dict, headers={
                'Authorization': "key=AAAASAYM3VY:APA91bH4xdLqY5mgmzixt9NAXD5SQ3RNyKR05Q428eXVWPv6-MHV-baWUBGZ8WGyZzTko-9m63UpDUm-7IcmI8IG3Q7AZINm0-8PY9btdAdUCfsNJOpUUp-MVI_l8QvOPMJbq7X7nFzJ",
                'Content-Type': "application/json"})
            print("sent")
        except  Exception as e:
            print(e)