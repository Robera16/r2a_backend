# chat/routing.py
from django.urls import re_path

from . import consumer

websocket_urlpatterns = [
    re_path(r"ws/chat/user/(?P<username>[-\w]+)/group/(?P<group_id>\d+)/$", consumer.ChatsConsumer),

    re_path(r"ws/chat/user/(?P<username>[-\w]+)/other_user/(?P<user_id>\d+)/$", consumer.OneToOneChatConsumer),
]
# user/(?P<username>[-\w]+)/group/(?P<group_id>\d+)/$
