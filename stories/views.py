from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from .serializers import MyStroriesSerialier, UsersListSerializer, StoriesListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, parser_classes
from django.shortcuts import get_object_or_404
from .models import Story
from django.contrib.auth import get_user_model
from friendship.models import Follow
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser

User = get_user_model()

#Get all user list who are being followed by current user and having stories including current user 
@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def my_stories(request):
    list_with_stories = Story.get_user_stories(request.user)
    context  = {'request':request} 
    serialize =  UsersListSerializer(instance=list_with_stories, many=True, context=context)
    return Response(serialize.data)

#get all stories of a particular user
@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def get_user_stories(request, pk):
    context  = {'request':request} 
    user = get_object_or_404(User.objects.all(), pk=pk)
    stories = user.stories.all().order_by('-created_at')
    serialize = StoriesListSerializer(instance=stories, many=True, context=context)
    return Response(
        serialize.data
    )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def update_seen_by(request, pk):
    user = request.user
    story = get_object_or_404(Story.objects.all(), pk=pk)
    if story.user != user and  user not in story.seen_by.all():
        story.seen_by.add(user)
        story.save()
        return Response(
            "added sucessFully"
        )
    else:
        return Response("already added or own story")
        
@api_view(['POST'])
@permission_classes([IsAuthenticated,])
@parser_classes([MultiPartParser, FormParser, FileUploadParser,])
def create_story(request):
    request.POST._mutable = True
    context  = {'request':request} 
    data = request.data
    data['user'] = request.user.id
    serialze = MyStroriesSerialier(data=data, context = context)
    if serialze.is_valid(raise_exception=True):
        serialze.save()
    return Response({
        "data": serialze.data
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated,])
def delete_user_post(request, pk):
    story = get_object_or_404(Story.objects.all(), pk=pk)
    if (story.user == request.user):
        story.delete()
        return Response({
            "Deleted Successfully"
        })
    else :
        return Response({
            "detail": "Cannot Delete Other Users Story"
        }, status=status.HTTP_403_FORBIDDEN)