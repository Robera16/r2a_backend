from django.urls import path
from .views import (
    create_request, FriendsRequestsListView, FriendsListView, 
    AcceptRequestView, accept_request, reject_request, SentRequestsList,
    friend_request_count, RejectedRequestsListView,
    unfriend_user, check_is_friend, UnRejectedRequestList, delete_request
    )

urlpatterns = [
    path('create/', create_request),
    path('requests_list/', FriendsRequestsListView.as_view()),
    path('list/', FriendsListView.as_view() ),
    path('accept_request/<int:pk>/', accept_request),
    path('reject_request/<int:pk>/', reject_request),
    path('sent_request_list/', SentRequestsList.as_view()),
    path('requests_count/', friend_request_count),
    path('rejected_list/', RejectedRequestsListView.as_view()),
    path('unfriend/', unfriend_user),
    path('check_friends/', check_is_friend),
    path('unrejected_requests_list/', UnRejectedRequestList.as_view()),
    path('delete_request/<int:pk>/', delete_request)

]
