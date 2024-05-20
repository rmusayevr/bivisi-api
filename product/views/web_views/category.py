from rest_framework.generics import ListAPIView
from ...models import Category
from ...serializers import CategoryWebSerializer
from services.pagination import InfiniteScrollPagination


class CategoryWebListView(ListAPIView):
    queryset = Category.objects.filter(parent_name__isnull=True)
    serializer_class = CategoryWebSerializer
    search_fields = ['name']
    pagination_class = InfiniteScrollPagination