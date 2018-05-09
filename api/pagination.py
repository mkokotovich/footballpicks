from rest_framework.pagination import PageNumberPagination


class APIPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size = 25
    max_page_size = 100
    page_size_query_param = 'page_size'
    last_page_strings = ()
