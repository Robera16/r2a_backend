from rest_framework.pagination import PageNumberPagination

class PollsPagination(PageNumberPagination):
    page_size = 10