from rest_framework.pagination import PageNumberPagination

#TODO: Change to 15
class FriendsPagination(PageNumberPagination):
    page_size = 11