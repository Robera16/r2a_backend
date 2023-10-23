from django.shortcuts import render
from .serializers import NotificationSerialier
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .pagination import NotificationPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes


class NotificationListView(ListAPIView):
    permission_classes =  (IsAuthenticated, )
    serializer_class = NotificationSerialier
    pagination_class = NotificationPagination

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at', 'seen')


class UnSeenNotificationsCount(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        count = Notification.objects.filter(user=self.request.user, seen=False).count()
        data = {"count": count}
        return Response(data)

class MarkAllSeen(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        Notification.objects.filter(user=self.request.user, seen=False).update(seen=True)
        return Response("updated all objects")







from django.http import JsonResponse
from twilio.twiml.voice_response import VoiceResponse

from django.conf import settings
from twilio.rest import Client

from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

# Twilio setup
TWILIO_ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
TWILIO_API_SECRET= settings.TWILIO_API_SECRET

# client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@api_view(['GET'])
# @permission_classes([IsAuthenticated,])
def make_call(request):
    user = request.user

    # Generate a Twilio token with VideoGrant
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_API_SECRET)
    token.identity = user.username
    video_grant = VideoGrant(room='default')
    token.add_grant(video_grant)

    return Response({'token': token.to_jwt()})