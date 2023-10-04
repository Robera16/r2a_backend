from django.urls import path
from .views import my_stories, create_story, delete_user_post, get_user_stories, update_seen_by

urlpatterns = [
    path('my_stories/', my_stories), #get all  users current user is following with stories also includes current user
    path('create/', create_story),
    path('delete/<int:pk>/', delete_user_post),
    path('user/<int:pk>/', get_user_stories) ,
    path('update_seen_by/<int:pk>/', update_seen_by)
]