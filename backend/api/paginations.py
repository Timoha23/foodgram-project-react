from rest_framework import pagination


class PageNumberAsLimitOffset(pagination.PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "limit"
    page_size = 1
