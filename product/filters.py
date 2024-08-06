import django_filters
from django.db.models import Q
from product.models import ProductVideoType


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name='price', method='filter_min_price')
    max_price = django_filters.NumberFilter(
        field_name='price', method='filter_max_price')

    class Meta:
        model = ProductVideoType
        fields = ['min_price', 'max_price', 'product__in_sale', 'product__is_premium',
                  'product', 'product_type', 'product__category']

    def filter_min_price(self, queryset, name, value):
        return queryset.filter(
            Q(product__in_sale=True, product__final_price__gte=value) |
            Q(product__in_sale=False, product__price__gte=value)
        )

    def filter_max_price(self, queryset, name, value):
        return queryset.filter(
            Q(product__in_sale=True, product__final_price__lte=value) |
            Q(product__in_sale=False, product__price__lte=value)
        )
