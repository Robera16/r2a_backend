from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import UserProfile, PhoneOtp
import random

from firebase_admin import firestore

from friendship.signals import friendship_request_accepted

from django.conf import settings
import os

User = get_user_model()

anonymous_avatars = [
    'icons/incognito/incognito9.png',
    'icons/incognito/incognito8.png',
    'icons/incognito/incognito7.png',
    'icons/incognito/incognito6.png',
    'icons/incognito/incognito5.png',
    'icons/incognito/incognito4.png',
    'icons/incognito/incognito3.png',
    'icons/incognito/incognito1.png',
    'icons/incognito/incognito10.png',
    'icons/incognito/incognito11.png',
    'icons/incognito/incognito12.png',
    'icons/incognito/incognito13.png',
    'icons/incognito/incognito14.png',
    'icons/incognito/incognito15.png',
    'icons/incognito/incognito16.png',
    'icons/incognito/incognito17.png'
]

anonymous_avatar = 'user_avatars/hide.gif'

profile_avatars = [
'icons/avatars/r2a17.png',
'icons/avatars/r2a16.png',
'icons/avatars/r2a15.png',
'icons/avatars/r2a13.png',
'icons/avatars/r2a12.png',
'icons/avatars/r2a11.png',
'icons/avatars/r2a10.png',
'icons/avatars/r2a9.png',
'icons/avatars/r2a8.png',
'icons/avatars/r2a7.png',
'icons/avatars/r2a6.png',
'icons/avatars/r2a5.png',
'icons/avatars/r2a4.png',
'icons/avatars/r2a3.png',
'icons/avatars/r2a2.png',
'icons/avatars/r2a1.png'
]

profile_avatar = 'user_avatars/user.gif'

db = firestore.client()

def create_fireStrore_user(data, docId):
    doc_name = docId
    chat_room_doc = db.collection(u'users').document(doc_name)
    chat_room_doc.set(data)

#Create profile to user whenever created, add user to collections on fireStore
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, avatar=profile_avatar, anonymous_avatar=anonymous_avatar)
        data ={
            u'phoneNumber': instance.phone_number,
            u'avatarUrl': instance.profile.avatar.url,
            u'r2aId': instance.id,
            u'firstName': instance.first_name,
            u'timestamp': firestore.SERVER_TIMESTAMP
          }
        docId = str(instance.id)
        create_fireStrore_user(data, docId)

#TODO: Change this to on create 
#"""Make Can create permission to false on create of a user if he/she is political or medical""""
# @receiver(pre_save, sender = User)
# def add_create_status(sender, instance, **kwargs ):
#     if instance.role == 1 or instance.role == 2:
#         instance.can_create = False

@receiver(post_delete, sender=User)
def delete_phone_otp(sender, instance, using, **kwargs):
    phoneotp = PhoneOtp.objects.filter(phone_number__iexact = instance.phone_number)
    if phoneotp.exists():
        phone = phoneotp.first()
        phone.delete()

@receiver(post_save, sender=User)
def updateUserData(sender, instance, **kwargs):
    db.collection(u'users').document(str(instance.id)).update({
        u'avatarUrl': instance.profile.avatar.url,
        u'firstName': instance.first_name
    })

post_save.connect(create_user_profile, sender=User)
post_delete.connect(delete_phone_otp, sender=User)
# pre_save.connect(add_create_status, sender=User)