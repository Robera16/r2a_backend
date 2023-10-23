from django.urls import path
from .views import NotificationListView, UnSeenNotificationsCount, MarkAllSeen, make_call

urlpatterns =[
    path('list/', NotificationListView.as_view()),
    path('count/', UnSeenNotificationsCount.as_view()),
    path('mark_all_seen/', MarkAllSeen.as_view()),
    path('make_call/', make_call, name='make_call'),
]