from rest_framework.pagination import PageNumberPagination

class EventsPagination(PageNumberPagination):
    page_size = 15