from django.urls import path
from .views import ( create_follower, FollowersListView, FollowingListView,
                    UnFollowView, UserFollowingListView, UserFollowersListView,
                    get_chat_room, RemoveFollowerView, get_follower_chat_rooms )

urlpatterns = [
    path('create/', create_follower),
    path('followers_list/', FollowersListView.as_view()),
    path('following_list/', FollowingListView.as_view()),
    path('unfollow/', UnFollowView.as_view()),
    path('users/followers_list/<int:pk>/', UserFollowersListView.as_view()),
    path('users/following_list/<int:pk>/', UserFollowingListView.as_view()),
    path('chatroom_id/<int:pk>/', get_chat_room),
    path('remove/', RemoveFollowerView.as_view()),
    path('search_chat_rooms/', get_follower_chat_rooms)
]