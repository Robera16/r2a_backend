from django.shortcuts import render
from .serializers import NotificationSerialier
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .pagination import NotificationPagination
from rest_framework.response import Response

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
