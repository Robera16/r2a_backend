from django.shortcuts import render
from friendship.models import Follow
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from .pagination import FollowersPagination
from .serializers import FollowerslistSerializers, SearchedChatRoomsList
from firebase_admin import firestore
from django.db.models import Q
import os
import json
import requests
import pyotp
from rest_framework import status
from api_auth.models import UserProfile
from utils.notifications import send_push_notification

db = firestore.client()
User = get_user_model()
notification_url = os.environ['FIREBASE_MESSAGE_URL']

@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def create_follower(request):
    recipient = request.data.get('recipient_id')
    creator = request.user
    context  = {'request':request} 

    if recipient:
        recipient_user = get_object_or_404(User.objects.all(), pk=recipient)
        follow = Follow.objects.add_follower(request.user, recipient_user)
        context  = {'request':request}
        notification_dict = {
                        "collapse_key": "r2a",
                        "to": "token",
                        "notification": {
                            "title": "Following",
                            "body": "{name} started following you.".format(name=request.user.first_name)
                            },
                        "data": {
                            "click_action": "FLUTTER_NOTIFICATION_CLICK",
                            "friends" : {
                            "id" : request.user.id
                            }
                        },
                        "priority": 10
                    }
        send_push_notification(request.user, recipient_user, notification_dict)
        return Response({
            "status": "followShip Created",
            "data": FollowerslistSerializers(instance=follow.followee, context=context).data
        })
    else:
        return Response({
            "detail": "recipient_id is mandatory"
        }, status=status.HTTP_400_BAD_REQUEST)




class FollowersListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    pagination_class = FollowersPagination
    serializer_class = FollowerslistSerializers
    def get_queryset(self):
        user = User.objects.get(pk=self.request.user.id)
        return Follow.objects.followers(user=user)

#Searched users followers list
class UserFollowersListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    pagination_class = FollowersPagination
    serializer_class = FollowerslistSerializers
    def get_queryset(self):
        user = User.objects.get(pk=self.kwargs['pk'])
        return Follow.objects.followers(user=user)

#Searched users followings list
class UserFollowingListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    pagination_class = FollowersPagination
    serializer_class = FollowerslistSerializers
    def get_queryset(self):
        user = User.objects.get(pk=self.kwargs['pk'])
        return Follow.objects.following(user=user)

class FollowingListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    pagination_class = FollowersPagination
    serializer_class = FollowerslistSerializers
    def get_queryset(self):
        user = User.objects.get(pk=self.request.user.id)
        return Follow.objects.following(user=user)

#this is unfollow i can unfollow a user whome i have been following 
class UnFollowView(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        followee_id =  request.data.get('followee_id')
        followee = get_object_or_404(User.objects.all(), pk=followee_id)
        follow_status = Follow.objects.remove_follower(request.user, followee)
        if not follow_status:
            return Response({
                "detail": "Unfollow failed, are you following the provided user ?"
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({
            "detail": "Follower removed"
        })

#this remove followee remove user 'A' from following me ...
class RemoveFollowerView(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        followee_id =  request.data.get('followee_id')
        followee = get_object_or_404(User.objects.all(), pk=followee_id)
        follow_status = Follow.objects.remove_follower(followee, request.user)
        if not follow_status:
            return Response({
                "detail": "Remove follower failed, is provided user following you ?"
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({
            "detail": "Followee Removed"
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def get_chat_room(request, pk):
    requested_user = get_object_or_404(User.objects.all(), pk=pk)
    current_user = request.user
    if current_user == requested_user:
        return Response({"Cannot message your self"}, status=status.HTTP_406_NOT_ACCEPTABLE)
    doc_id =  get_or_create_room(current_user, requested_user)
    return Response({
        "room_id": doc_id 
    })


'''
  search with

    #TODO: longrun need to either do caching or store these chat rooms on db (stroing on db might be be wrong 
    as we also might have option to delete chatRooms)
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def get_follower_chat_rooms(request):
    try :
        current_user = request.user
        searched_chat_rooms = []
        if 'search' in request.query_params:
            search = request.query_params['search']
            users = User.objects.filter(Q(first_name__icontains = search) | Q(username__icontains = search)).distinct().exclude(id=current_user.id).exclude(admin=True).values('id', 'first_name', 'username', 'profile')
            profile_ids = list(d['profile'] for d in users )
            user_ids = list(d['id'] for d in users )
            user_first_names = list(d['first_name'] for d in users)
            user_names = list(d['username'] for d in users)
            chat_room_doc = db.collection(u'chatRoom').where(u'multitenant', u'==', False).where(u'users', u'array_contains', current_user.id).get()
            if chat_room_doc:
                for doc in chat_room_doc:
                    doc_users = doc.to_dict()['users']
                    doc_users.remove(current_user.id)
                    if doc_users[0] in user_ids:
                        index = user_ids.index(doc_users[0])
                        profile_id = profile_ids[index]
                        url = UserProfile.objects.get(id =profile_id).mainAvatar()
                        searched_chat_rooms.append({"chatRoomId": doc.id,"first_name": user_first_names[index], "user_name": user_names[index], "avatar_url": url, "userId": current_user.id, "tenantId": doc_users[0]})
            data = SearchedChatRoomsList(searched_chat_rooms, many=True)
            return Response({"ok": "Okay", "data": data.data})

        

    except Exception as e:
        print("Error: get_follower_chat_rooms -> ", e)
        return Response({"message": "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




def get_or_create_room(current_user, requested_user):
    chat_room_doc = db.collection(u'chatRoom').where(u'multitenant', u'==', False).where(u'users', u'array_contains', current_user.id).get()
    #Check if any chatRooms were created with current_user(logged in user)
    if chat_room_doc:
        #interate over all the chatRooms
        for doc in chat_room_doc:
            #Check if there is room with current user and requested user in if yes return the room id
            if(requested_user.id in doc.to_dict().get('users')):
                doc_id = doc.id
                return doc_id
        #there were no chat rooms with current_user and requested_user are part of so create new one
        #basically return did not happen
        return create_chat_room(current_user, requested_user)
    #There were no rooms at all with logged in user ...
    else:
        return create_chat_room(current_user, requested_user)


def create_chat_room(current_user, requested_user):
    totp = pyotp.TOTP('base32secret3232')
    key = totp.now()
    doc_name = current_user.first_name + '-' + requested_user.first_name + '--' + key
    doc_name = doc_name.replace(" ", "")
    chat_room_doc = db.collection(u'chatRoom').document(doc_name.replace(" ", ""))
    doc = chat_room_doc.set({
        u'last_message': "",
        u'multitenant': False,
        u'users': [current_user.id, requested_user.id],
        u'timestamp': firestore.SERVER_TIMESTAMP
    })
    return doc_name

    