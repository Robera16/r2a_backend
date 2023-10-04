from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from .serializers import PollSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from .pagination import PollsPagination
from .models import Poll, PollAnswer, Choice, PollComment
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404


class PollsListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PollSerializer
    pagination_class = PollsPagination
    def get_queryset(self):
        return Poll.objects.all().order_by('-created_at')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vote_or_remove(request, pk):
    poll = get_object_or_404(Poll.objects.all(), pk=pk)
    choice_id = request.data.get("choice_id")
    try:
        choice = get_object_or_404(Choice.objects.all(), pk=choice_id)
        #check if the supplied question and chocie are related or not  
        if choice.question == poll:
            # get if his users already voted
            try:
                user_answer = PollAnswer.objects.get(question=poll, user=request.user)
                # if his current choice is already there delete it
                if user_answer.choice == choice:
                    user_answer.delete()
                else:
                    #else add/replace the new the new choice with old one
                    user_answer.choice = choice
                    user_answer.save()
                    
            #if it does not exists create new one 
            except PollAnswer.DoesNotExist:
                PollAnswer.objects.create(question=poll, choice=choice, user = request.user)
            return Response({
                    "detail": "updated successfully"
                }, status=status.HTTP_200_OK)
        else:
            return Response({
                "detail": "the choice is not associated with the question"
            }, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({
            "detail": "Problem updating poll . Please try again later"
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def comment_poll(request, pk):
    poll = get_object_or_404(Poll.objects.all(), pk=pk)
    comment = request.data.get("message")
    try:
        PollComment.objects.create(question=poll, user=request.user, text=comment)
        return Response({
            "count": PollComment.objects.count(),
            "detail": "created Sucessully"
        })
    except :
        return Response({
            "detail": "Problem creating comments  . Please try again later"
        }, status=status.HTTP_400_BAD_REQUEST)

class CommentsListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CommentSerializer
    pagination_class = PollsPagination
    def get_queryset(self):
        return PollComment.objects.filter(question=self.kwargs['pk']).order_by('-created_at')

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, ])
def delete_comment(request, pk):
    comment = get_object_or_404(PollComment.objects.all(), pk=pk)
    if comment.user == request.user:
        comment.delete()
        return Response({
            "detail": "delete sucessfully",
            "count": PollComment.objects.count()
        })
    else:
        return Response({
            "detail": "Cannot delete other user comments"
        }, status=status.HTTP_403_FORBIDDEN)




