from django.urls import path
from .views import GroupView, UserGroups, GroupUsers, GroupMessagesView, MessageView

urlpatterns = [
    path('group/', GroupView.as_view()),
    path('group/<int:group>/',GroupView.as_view()),
    path('my_groups/', UserGroups.as_view()),
    path('group_users/<int:group>/', GroupUsers.as_view()),
    path('group_messages/<int:group>/', GroupMessagesView.as_view()),
    path('message/<int:message>/', MessageView.as_view())
]