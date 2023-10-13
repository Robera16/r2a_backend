from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import GroupSerializer, GroupMessageSerializer
from rest_framework import status
from rest_framework.generics import ListAPIView
from .pagination import GroupPagination, MessagesPagination
from .models import Group, GroupMessage
from django.contrib.auth import get_user_model
from friends.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, parser_classes

from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
User = get_user_model()


class GroupView(APIView):
    permission_classes = ([IsAuthenticated, ] )

    def get(self, request, group):
        data = request.data
        data['creator'] = request.user.id
        context  = {'request':request}
        room = get_object_or_404(Group.objects.all(), pk=group)
        serialize = GroupSerializer(room, context=context)
        return Response(serialize.data)
    
    def post(self, request):
        data = request.data
        data['creator'] = request.user.id
        context  = {'request':request}
        serialized = GroupSerializer(data=data, context=context)
        if serialized.is_valid(raise_exception=True):
            serialized.save()
            return Response(serialized.data)
        return Response("Some thing went wrong please try again", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, group):
        saved_post = get_object_or_404(Group.objects.all(), pk=group)
        data = request.data
        data['creator'] = request.user.id
        context  = {'request':request}
        serializer = GroupSerializer(instance=saved_post, data=data, context=context, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({
            "data": serializer.data
        })
    
    def delete(self, request, group):
        print('inside delete')
        group = get_object_or_404(Group.objects.all(), pk=group)
        print('group', group)
        group.delete()
        return Response(status=status.HTTP_200_OK)



class UserGroups(ListAPIView):
    permission_classes = ([IsAuthenticated, ] )
    pagination_class = GroupPagination
    serializer_class = GroupSerializer

    def get_queryset(self):
        return User.objects.get(pk=self.request.user.id).group_users.all()

class GroupUsers(ListAPIView):
    permission_classes = ([IsAuthenticated, ] )
    pagination_class = GroupPagination
    serializer_class = UserSerializer
    def get_queryset(self):
        group = get_object_or_404(Group.objects.all(), pk=self.kwargs['group'])
        return group.recepients.all()

class GroupMessagesView(ListAPIView):
    permission_classes = ([IsAuthenticated, ] )
    pagination_class = MessagesPagination
    serializer_class = GroupMessageSerializer
    def get_queryset(self):
        group = get_object_or_404(Group.objects.all(), pk=self.kwargs['group'])
        return group.messages.all()

class MessageView(APIView):
    permission_classes = ([IsAuthenticated, ] )

    def put(self, request, message):
        message = get_object_or_404(GroupMessage.objects.all(), pk=message)
        data = request.data
        context  = {'request':request}
        serialize = GroupMessageSerializer(instance=message, data=data, partial=True, context=context)
        if serialize.is_valid(raise_exception=True):
            serialize.save()
        return Response(serialize.data)
    
    def delete(self, request, message):
        message = get_object_or_404(GroupMessage.objects.all(), pk=message)
        message.delete()
        return Response(status=status.HTTP_200_OK)