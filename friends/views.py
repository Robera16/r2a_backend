from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from friendship.models import Friend, Follow, Block, FriendshipRequest
from .serializers import FriendsRequestListSerializers, FriendsListSerializers
from django.core import serializers
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from .pagination import FriendsPagination
from rest_framework import status
from firebase_admin import firestore
import os
import json
import requests

db = firestore.client()

notification_url = os.environ['FIREBASE_MESSAGE_URL']

User = get_user_model()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_request(request):
    recipient = request.data.get('recipient_id')
    message = request.data.get('message')
    creator = request.user
    context  = {'request':request} 
    if recipient and creator:
        recipient_user = User.objects.get(pk = recipient)
        if recipient_user:
            friend_request = Friend.objects.add_friend(
                creator,                               # The sender
                recipient_user,                        # The recipient
                message= message)
            serialized = FriendsRequestListSerializers(instance=friend_request, context=context)
            send_push_notification(request.user, recipient_user)
            return Response({
                "status": "ok",
                "message": "friend request created",
                "data": serialized.data
            })
        else:
            return Response({
                "status": "bad",
                "message": "user with id does not exists",
                "CODE": "USER_UNKNOWN"
            })
    else:
        return Response({
            "status": "bad",
            "message": "recipient_id is required field ",
            "CODE": "PARAM_REQUIRED_RECIPIENT_ID"
        })

class FriendsRequestsListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = FriendsRequestListSerializers
    pagination_class = FriendsPagination
    def get_queryset(self):
        data_user  = User.objects.get(pk = self.request.user.id)
        data = Friend.objects.unread_requests(user=data_user)
        return data

#TODO: Without blindly accepting the request need to check who is sending the request and is this the request he got
#because by mistake any body can accept a request...
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accept_request(request, pk):
    context  = {'request':request} 
    friend_request = FriendshipRequest.objects.get(pk=pk)
    if friend_request:
        from_user = friend_request.from_user
        friend_request.accept()
        serialized = FriendsListSerializers(instance=from_user, context=context)
        return Response({
            "status": "ok",
            "message": "Friend Request accepted",
            "data": serialized.data
        })
    else:
        return Response({
            "status": "bad",
            "message": "...."
        })   

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_request(request, pk):
    request = get_object_or_404(FriendshipRequest.objects.all(), pk=pk)
    request.delete()
    return Response({"message": "Successfully Deleted"}, status=status.HTTP_200_OK)

#TODO: implement same work flow as above
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reject_request(request, pk):
    request = FriendshipRequest.objects.get(pk=pk)
    if request:
        request.reject()
        return Response({
            "status": "ok",
            "message": "Friend Request Rejected"
        })
    else:
        return Response({
            "status": "bad",
            "message": "...."
        })    


class AcceptRequestView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(request, pk):
        request = FriendshipRequest.objects.get(pk=pk)
        if request:
            request.accept()
            return Response({
                "status": "ok",
                "message": "Friend Request accepted"
            })
        else:
            return Response({
                "status": "bad",
                "message": "...."
            })


class FriendsListView(ListAPIView):  
    permission_classes = (IsAuthenticated, )
    serializer_class = FriendsListSerializers
    pagination_class = FriendsPagination
    def get_queryset(self):
        return sorted(Friend.objects.friends(self.request.user), key=lambda data: data.created_at)

class SentRequestsList(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = FriendsRequestListSerializers
    pagination_class = FriendsPagination
    def get_queryset(self):
        return Friend.objects.sent_requests(user=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friend_request_count(request):
    count = Friend.objects.unrejected_request_count(user=request.user)
    return Response({
        "status": "ok",
        "message": "requests count",
        "data": count
    })

class UnRejectedRequestList(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = FriendsRequestListSerializers
    pagination_class = FriendsPagination
    def get_queryset(self):
        return Friend.objects.unrejected_requests(user=self.request.user)

class RejectedRequestsListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = FriendsRequestListSerializers
    pagination_class = FriendsPagination
    def get_queryset(self):
        return Friend.objects.rejected_requests(user=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfriend_user(request):
    unfriend_user_id = request.data.get('recipient_id')
    recipient_user = User.objects.get(pk=unfriend_user_id)
    if recipient_user:
        Friend.objects.remove_friend(request.user, recipient_user)
        return Response({
            "status": "ok",
            "message": "unfriend user with id unfriend_user_id sucess",
        })
    else:
        return({
            "status": "bad",
            "message": "user not found"
        })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_is_friend(request):
    unfriend_user_id = request.data.get('recipient_id')
    recipient_user = User.objects.get(pk=unfriend_user_id)
    if recipient_user:
        data = Friend.objects.are_friends(request.user, recipient_user)
        if data == True:
            return Response({
                "status": "ok",
                "message": "are friends",
                "data": True
            })
        else: 
            return Response({
                "status": "ok",
                "message": "are not friends",
                "data": False
            })
    else:
        return({
            "status": "bad",
            "message": "user not found"
        })

def send_push_notification(from_user, to_user):
    user = db.collection(u'users').where(u'r2aId', u'==', to_user.id).limit(1).get()
    if(len(user) > 0):
        token = user[0].to_dict().get("pushToken")
        request_dict = {
                        "collapse_key": "r2a",
                        "to": token,
                        "notification": {
                            "title": "Friend Request",
                            "body": "You have a request from {name}".format(name=from_user.first_name)
                            },
                        "data": {
                            "click_action": "FLUTTER_NOTIFICATION_CLICK",
                            "friends" : {
                            "id" : from_user.id
                            }
                        },
                        "priority": 10
                    }
        request_dict = json.dumps(request_dict)
        try:
            resp = requests.post(notification_url, request_dict, headers={
                'Authorization': "key=AAAASAYM3VY:APA91bH4xdLqY5mgmzixt9NAXD5SQ3RNyKR05Q428eXVWPv6-MHV-baWUBGZ8WGyZzTko-9m63UpDUm-7IcmI8IG3Q7AZINm0-8PY9btdAdUCfsNJOpUUp-MVI_l8QvOPMJbq7X7nFzJ",
                'Content-Type': "application/json"})
        except  Exception as e:
            print(e)
