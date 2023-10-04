from rest_framework.pagination import PageNumberPagination

class GroupPagination(PageNumberPagination):
    page_size = 15

class MessagesPagination(PageNumberPagination):
    page_size = 15