from django.urls import path
from .views import NotificationListView, UnSeenNotificationsCount, MarkAllSeen

urlpatterns =[
    path('list/', NotificationListView.as_view()),
    path('count/', UnSeenNotificationsCount.as_view()),
    path('mark_all_seen/', MarkAllSeen.as_view()),
]