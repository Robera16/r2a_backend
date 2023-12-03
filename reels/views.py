from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, parser_classes
from django.shortcuts import get_object_or_404
from .models import *
from django.contrib.auth import get_user_model
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from .pagination import *
User = get_user_model()



#Create a new reel
class CreateReel(APIView):
    permission_classes = (IsAuthenticated, )
    parser_classes = (MultiPartParser, FormParser, FileUploadParser, )

    def post(self, request):   
        self.request.POST._mutable = True
        reel = request.data
        reel['user_id'] = request.user.id
        context  = {'request':request} 
        serialze = ReelsSerializer(data=reel, context = context)
        if serialze.is_valid(raise_exception=True):
            serialze.save()
        return Response({
            "status": "ok",
            "message": "Reel have been created sucessfully",
            "data": serialze.data
        })

# Update/Delete reel
class UpdateReelView(APIView):
    
    def put(self, request, pk):
        reel = get_object_or_404(Reel.objects.all(), pk=pk)
        data = request.data
        context  = {'request':request} 
        serializer = ReelsSerializer(instance=reel, data=data, partial=True, context = context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({
            "status": "ok",
            "message": "Reel has been Updated",
            "data": serializer.data
        })
    
    
    def delete(self, request, reel_id):
        reel = get_object_or_404(Reel.objects.all(), pk=reel_id)
        reel.delete()
        return Response({
            "status": "ok",
            "message": "Reel Deleted Sucessfully"
        })



# Get all reels in which the current user follows
class ReelsListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ReelsSerializer
    pagination_class = ReelsPagination
    def get_queryset(self):
        if 'search' in self.request.query_params:
            return Reel.objects.filter(description__icontains = self.request.query_params['search'] ).order_by('-created_at')
        else :
            return Reel.objects.all()

#Get a specific Reel
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reel(request, pk):
    context  = {'request':request} 
    reel_data = get_object_or_404(Reel.objects.all(), pk=pk)
    serializer = ReelsSerializer(reel_data, context = context)
    return Response({
        "status": "ok",
        "message": "reel detail",
        "data": serializer.data
    })

# Get all reels in which the current user follows
class UserReelsListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ReelsSerializer
    def get_queryset(self):
        try:
            pk = self.kwargs.get('pk') 
            user_reels = Reel.objects.filter(user_id=pk)
            return user_reels
        except:
            return []

# Get all saved reels of the current user
class SavedReels(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ReelsSerializer
    pagination_class = ReelsPagination
    def get_queryset(self):
        try:
            user = self.request.user
            data = user.saved_reels.values('reel_id').order_by('-created_at')
            reels = list(d['reel_id'] for d in data )
            return Reel.objects.filter(id__in=reels).order_by('-created_at')
        except:
            return []


# Save/Unsave reel
class SaveReel(APIView):

    def post(self, request, reel_id):
        reel = get_object_or_404(Reel.objects.all(), pk=reel_id)
        try:
            SavedReel.objects.get(user_id=request.user, reel_id=reel).delete()
        except SavedReel.DoesNotExist:
            SavedReel.objects.create(user_id=request.user, reel_id=reel)
        return Response({
            "status": "ok",
            "message": "updated sucessfully"
        })

# Get all comments of specific reel
class ReelCommentsListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ReelCommentsSerializer
    pagination_class = ReelCommentsPagination

    def get_queryset(self):
        try:
            return Reel.objects.filter(pk=self.kwargs['reel_id']).first().comments.all().order_by("-created_at")
        except:
             return Response({
                "status": "bad",
                "message": "Comment not found"
            })
# Post comment for specific reel
class ReelCommentView(APIView):
    permission_classes = ([IsAuthenticated, ])

    def post(self, request, reel_id):
        message = request.data.get('message')
        if message:
            reel = get_object_or_404(Reel.objects.all(), pk=reel_id)
            context  = {'request':request}
            comment = ReelComments.objects.create(reel_id = reel, user_id = self.request.user, message = message)
            serialized = ReelCommentsSerializer(comment, context=context)
            return Response({
                "status": "ok",
                "message": "Comment created sucessfully",
                "data": serialized.data
            })
        else:
            return Response({
                "status": "bad",
                "message": "Message param expected"
            })


# Like/Unlike specific reel comment
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_or_unlike_comment(request, comment_id):
    comment = get_object_or_404(ReelComments.objects.all(), pk=comment_id)
    try:
        ReelCommentLike.objects.get(user_id=request.user, comment_id=comment).delete()
    except ReelCommentLike.DoesNotExist:
        ReelCommentLike.objects.create(user_id=request.user, comment_id=comment)
    return Response({
        "status": "ok",
        "message": "updated sucessfully"
    })

# Share reel
class ReelShareView(APIView):
    permission_classes = ([IsAuthenticated, ])

    def post(self, request, reel_id):
        try:
            reel = get_object_or_404(Reel.objects.all(), pk=reel_id)
            context  = {'request':request}
            share = ReelShares.objects.create(reel_id = reel, user_id = self.request.user)
            serialized = ReelShareSerializer(share, context=context)
            return Response({
                "status": "ok",
                "message": "Reel shared sucessfully",
                "data": serialized.data
            })
        except:
            return Response({
                "status": "bad",
                "message": "Error happend during sharing"
            })


# Like/Unlike specific reel
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_or_unlike_reel(request, reel_id):
    reel = get_object_or_404(Reel.objects.all(), pk=reel_id)
    try:
        ReelLikes.objects.get(user_id=request.user, reel_id=reel).delete()
    except ReelLikes.DoesNotExist:
        ReelLikes.objects.create(user_id=request.user, reel_id=reel)
    return Response({
        "status": "ok",
        "message": "updated sucessfully"
    })