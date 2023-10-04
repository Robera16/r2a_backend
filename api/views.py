from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PostsSerializers, CommentsSerializers, CommentSerializer, UsersListSerializers, UsersSerializers, AttachmentsSerializers, SingleAttachmentSerializer
from django.shortcuts import get_object_or_404
from .models import Post, Attachment, Likes, Comments, SavedPost
from rest_framework import status
from .pagination import PostsPagination
from django.contrib.auth import get_user_model
import pdb
from django.db.models import Q
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from .uploder import updateFile
from notifications.models import Notification

User = get_user_model()
#Create a new POST
class UserPosts(APIView):
    permission_classes = (IsAuthenticated, )
    parser_classes = (MultiPartParser, FormParser, FileUploadParser, )

    def post(self, request):
        self.request.POST._mutable = True
        post = request.data
        post['user_id'] = request.user.id
        context  = {'request':request} 
        serialze = PostsSerializers(data=post, context = context)
        if serialze.is_valid(raise_exception=True):
            serialze.save()
        return Response({
            "status": "ok",
            "message": "Post have been saved sucessfully",
            "data": serialze.data
        })

class UploadToFirebaseStorage(APIView):
    permission_classes = (IsAuthenticated, )
    parser_classes = (MultiPartParser, FormParser, FileUploadParser, )

    def post(self, request):
        self.request.POST._mutable = True
        file_url = updateFile(request.FILES['file'], request.user.id)
        return Response({
            "url": file_url
        })

class UploadAttachment(APIView):
    parser_classes = (MultiPartParser, FormParser, FileUploadParser, )
    def post(self, request):
        data = request.data
        serialize = SingleAttachmentSerializer(data = data)
        if (serialize.is_valid(raise_exception=True)):
            serialize.save()
        return Response(serialize.data)

#Get list of all user specific posts based on category (political/medical)
class UserPostsCategoryListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostsSerializers
    pagination_class = PostsPagination
    def get_queryset(self):
        return Post.objects.filter(category=self.kwargs['category'], user_id = self.request.user).order_by('-created_at')

class MyConstituencyPostView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostsSerializers
    pagination_class = PostsPagination
    def get_queryset(self):
        return Post.objects.filter(category=1, constituency = self.request.user.constituency_id).order_by('-created_at')

class PostsCategoryListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostsSerializers
    pagination_class = PostsPagination
    def get_queryset(self):
        status = None
        if 'status' in self.request.query_params:
            if self.request.query_params['status'] == '1':
                status = True
            elif self.request.query_params['status'] == '2':
                status = False
            else:
                status = None
        if 'constituency' in self.request.query_params:
            return Post.get_constituency_posts(self.request.query_params['constituency'], status=status).filter(category=self.kwargs['category'])
        elif 'district' in self.request.query_params:
            return Post.get_district_posts(self.request.query_params['district'], status=status).filter(category=self.kwargs['category'])
        elif 'state' in self.request.query_params:
            return Post.get_state_posts(self.request.query_params['state'], status=status).filter(category=self.kwargs['category'])
        else :
            if status is not None:
                return Post.objects.filter(category=self.kwargs['category'], clarified=status).order_by('-created_at') 
            else:
                return Post.objects.filter(category=self.kwargs['category']).order_by('-created_at') 

#These are all user specific views (can perfrom action on only this user created items)
class UserPostView(APIView):
    #update a specific Post
    def put(self, request, pk):
        saved_post = get_object_or_404(Post.objects.all(), pk=pk)
        data = request.data
        context  = {'request':request} 
        serializer = PostsSerializers(instance=saved_post, data=data, partial=True, context = context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({
            "status": "ok",
            "message": "Post has been Updated",
            "data": serializer.data
        })
    
    #Delete a specific post
    def delete(self, request, pk):
        saved_post = get_object_or_404(Post.objects.all(), pk=pk)
        saved_post.delete()
        return Response({
            "status": "ok",
            "message": "Sucessfully Deleted Post"
        })

#this is also specific to user he can delete only his posts attachment only
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_attachment(request, pk):
    attachment = get_object_or_404(Attachment.objects.all(), pk=pk)
    if attachment.post_id.user_id == request.user:
        # attachment.attachment.delete(save=False)
        attachment.delete()
        return Response({
            "status": "ok",
            "message": "Attachment is deleted"
        })
    else:
        return Response({
            "status": "bad"
        }, status=status.HTTP_401_UNAUTHORIZED)

#Get a specific Post
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_post(request, pk):
    context  = {'request':request} 
    post_data = get_object_or_404(Post.objects.all(), pk=pk)
    serializer = PostsSerializers(post_data, context = context)
    return Response({
        "status": "ok",
        "message": "post detail",
        "data": serializer.data
    })

#TODO: implement filter on new feed 
#Verify if this filters  are  optimal 
#List all posts 
class PostsListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostsSerializers
    pagination_class = PostsPagination
    def get_queryset(self):
        if 'search' in self.request.query_params:
            return Post.objects.filter(description__icontains = self.request.query_params['search'] ).order_by('-created_at')
        else :
            return Post.get_regular_posts(self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def like_or_dislike_post(request, pk):
    post = get_object_or_404(Post.objects.all(), pk=pk)
    try:
        Likes.objects.get(user_id=request.user, post_id=post).delete()
    except Likes.DoesNotExist:
        Likes.objects.create(user_id=request.user, post_id=post)
    return Response({
        "status": "ok",
        "message": "updated sucessfully"
    })

class PostCommentsListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CommentsSerializers
    pagination_class = PostsPagination

    def get_queryset(self):
        return Post.objects.filter(pk=self.kwargs['post_id']).first().comments.all().order_by("-created_at")


class PostCommentView(APIView):
    permission_classes = ([IsAuthenticated, ])

    def post(self, request, pk):
        message = request.data.get('message')
        if message:
            post = get_object_or_404(Post.objects.all(), pk=pk)
            context  = {'request':request}
            comment = Comments.objects.create(message = message, post_id = post, user_id = self.request.user)
            serialized = CommentsSerializers(comment, context=context)
            return Response({
                "status": "ok",
                "message": "Comment Created sucessfully",
                "data": serialized.data
            })
        else:
            return Response({
                "status": "bad",
                "message": "Message param expected"
            })

class EditDeleteCommentView(APIView):
    permission_classes = ([IsAuthenticated, ])

    def delete(self, request, pk):
        comment = get_object_or_404(Comments.objects.all(), pk = pk, user_id = request.user)
        comment.delete()
        return Response({
            "status": "ok",
            "message": "Comment Deleted sucessfully"
        })

    def put(self, request, pk):
        saved_comments =  get_object_or_404(Comments.objects.all(), pk=pk, user_id = request.user)
        data = request.data
        serializer = CommentSerializer(instance=saved_comments, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({
            "status": "ok",
            "message": "comment updated",
            "data": serializer.data
        })
## current_user all
## View_user , {first_name, last_name}, id, avatar, cons, anonymous, role, district
## edit_user  no phone no email

class UserView(APIView):
    def get(self, request, pk):
        user_data = get_object_or_404(User.objects.all(), pk=pk)
        context  = {'request':request} 
        serializer = UsersSerializers(user_data, context=context)
        return Response({
            "status": "ok",
            "message": "User detail",
            "data": serializer.data
        })

class UsersListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UsersListSerializers
    pagination_class = PostsPagination
    def get_queryset(self):
        search = self.request.query_params.get('search')
        if search:
            #| Q(email__icontains = search) add this after first name if email filter is also reqyured ..
            return User.objects.filter(Q(first_name__icontains = search) | Q(username__icontains = search)).distinct().exclude(id=self.request.user.id).exclude(admin=True).order_by("-created_at")
        else:
            return []


class ProfileView(ListAPIView):
    parser_classes = (MultiPartParser, FormParser, FileUploadParser, )
    def put(self, request):
        context  = {'request':request}
        serializer = UsersSerializers(instance=request.user, data=request.data, partial=True, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({
            "status": "ok",
            "message": "user has been Updated",
            "data": serializer.data
        })

    def get(self, request):
        context  = {'request':request} 
        serializer = UsersSerializers(request.user, context=context)
        return Response({
            "status": "ok",
            "message": "User detail",
            "data": serializer.data
        })

class MyRecentPostsListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostsSerializers
    pagination_class = PostsPagination
    def get_queryset(self):
        return Post.objects.filter(user_id = self.request.user).order_by("-created_at")
    
class UserRecentPostViewList(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostsSerializers
    pagination_class = PostsPagination

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User.objects.all(), pk=user_id)
        return Post.objects.filter(user_id = user).order_by("-created_at")


class ClarifiedToogleView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, pk):
        print(pk)
        post = get_object_or_404(Post.objects.all(), pk=pk)
        post.clarified = not post.clarified
        post.save()
        context  = {'request':request} 
        serializer = PostsSerializers(post, context = context)
        return Response(serializer.data)

class MyDistrictPostView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostsSerializers
    pagination_class = PostsPagination
    def get_queryset(self):
        district = self.request.user.constituency_id.district_id
        return Post.objects.filter(category=2, district = district).order_by('-created_at')

     
class MyNewsFeed(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostsSerializers
    pagination_class = PostsPagination
    def get_queryset(self):
        return Post.objects.filter(user_id = self.request.user, category=4).order_by('-created_at')

class UserTaggedPosts(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostsSerializers
    pagination_class = PostsPagination
    def get_queryset(self):
        user_id = self.kwargs['pk']
        user = get_object_or_404(User.objects.all(), pk=user_id)
        return user.tagged.all().order_by('-created_at')

class MyTaggedPosts(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostsSerializers
    pagination_class = PostsPagination
    def get_queryset(self):
        user = self.request.user
        return user.tagged.all().order_by('-created_at')

class SavePost(APIView):

    def get(self, request, pk):
        post = get_object_or_404(Post.objects.all(), pk=pk)
        try:
            SavedPost.objects.get(user=request.user, post=post).delete()
        except SavedPost.DoesNotExist:
            SavedPost.objects.create(user=request.user, post=post)
        return Response({
            "status": "ok",
            "message": "updated sucessfully"
        })

class SavedPosts(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostsSerializers
    pagination_class = PostsPagination
    def get_queryset(self):
        try:
            user = self.request.user
            # fetch all saved posts (posts id) by a user
            data = user.saved_posts.values('post_id').order_by('-created_at')
            # selecting post_id is like post.id.
            posts = list(d['post_id'] for d in data )
            return Post.objects.filter(id__in=posts).order_by('-created_at')
        # if any error send empty response
        except:
            print("some error in SavedPosts -> api/views")
            return []
