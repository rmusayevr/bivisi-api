from rest_framework.pagination import LimitOffsetPagination



class InfiniteScrollPagination(LimitOffsetPagination):
    default_limit = 12  # Default number of items per page
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 1000  # Maximum number of items per page
