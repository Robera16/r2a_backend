from rest_framework.pagination import PageNumberPagination

#TODO: Change to 15
class FollowersPagination(PageNumberPagination):
    page_size = 10