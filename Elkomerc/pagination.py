from rest_framework import pagination

class CFEAPIPagination(pagination.PageNumberPagination):
    page_size = 10