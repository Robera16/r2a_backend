from rest_framework.pagination import PageNumberPagination

#TODO: Change to 15
class StoriesPagination(PageNumberPagination):
    page_size = 11