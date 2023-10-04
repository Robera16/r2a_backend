from rest_framework.pagination import PageNumberPagination

#TODO: change to 15
class PostsPagination(PageNumberPagination):
    page_size = 10