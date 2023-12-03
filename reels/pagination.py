from rest_framework.pagination import PageNumberPagination

class ReelsPagination(PageNumberPagination):
    page_size = 15

class ReelCommentsPagination(PageNumberPagination):
    page_size = 40