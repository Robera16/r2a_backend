from django.urls import path
from .views import *

urlpatterns = [
    path('create_reel/', CreateReel.as_view()),
    path('delete_reel/<int:reel_id>/', UpdateReelView.as_view()),
    path('all/', ReelsListView.as_view()),
    path('reel/<int:pk>/', get_reel),
    path('user_reel/<int:pk>/', UserReelsListView.as_view()),
    path('saved_reels/',SavedReels.as_view()),
    path('save_reel/<int:reel_id>/', SaveReel.as_view()),
    path('reel_comments/<int:reel_id>/', ReelCommentsListView.as_view()),
    path('create_comment/<int:reel_id>/', ReelCommentView.as_view()),
    path('like_comment/<int:comment_id>/', like_or_unlike_comment),
    path('like_unlike/<int:reel_id>/', like_or_unlike_reel),  
    path('share_reel/<int:reel_id>/', ReelShareView.as_view()),  
]