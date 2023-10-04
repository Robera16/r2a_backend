from friendship.signals import friendship_request_accepted
from django.dispatch import receiver
from friendship.models import Friend, Follow, Block, FriendshipRequest
from django.conf import settings
import os
import pyotp

from firebase_admin import firestore
from friendship.signals import friendship_request_accepted, friendship_removed


# db = firestore.client()


# #@FRIENSHIPHERE TODO: 
# #Whenever firend request is accepted create a group on fireStore
# @receiver(friendship_request_accepted)
# def created_request(from_user, to_user, **kwargs):
#     totp = pyotp.TOTP('base32secret3232')
#     key = totp.now()
#     doc_name = from_user.first_name + '-' + to_user.first_name + '--' + key
#     chat_room_doc = db.collection(u'chatRoom').document(doc_name.replace(" ", ""))
#     chat_room_doc.set({
#         u'last_message': "",
#         u'multitenant': False,
#         u'users': [from_user.id, to_user.id],
#         u'timestamp': firestore.SERVER_TIMESTAMP
#     })

# #whenever a unfriend is done, we will delete the chat room with for those two users (one-to-one) and also all messages of that chat
# @receiver(friendship_removed)
# def request_deleted(from_user, to_user, **kwargs):
#     chat_room_doc = db.collection(u'chatRoom').where(u'multitenant', u'==', False).where(u'users', u'array_contains', from_user.id).get()
#     for doc in chat_room_doc:
#         if(to_user.id in doc.to_dict().get('users')):
#             doc_id = doc.id
#             db.collection(u'chatRoom').document(doc_id).delete()
#             messages = db.collection(u'message').where(u'groupId', u'==', doc_id).get()
#             for message in messages:
#                 msg_id = message.id
#                 print(msg_id)
#                 db.collection(u'message').document(msg_id).delete()
#             print(doc_id)