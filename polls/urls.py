from django.urls import path
from .views import PollsListView, vote_or_remove, comment_poll, CommentsListView, delete_comment 

urlpatterns = [
    path('list/', PollsListView.as_view()),
    path('vote/<int:pk>/', vote_or_remove),
    path('comment/<int:pk>/', comment_poll),
    path('comments/<int:pk>/', CommentsListView.as_view()),
    path('delete_comment/<int:pk>/', delete_comment)
]