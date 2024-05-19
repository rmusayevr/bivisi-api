import django_filters.rest_framework
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from services.pagination import InfiniteScrollPagination
from .serializers import FAQSerializer, SliderSerializer
from .models import FAQ, Slider



# Slider GET & POST
class SliderListCreateAPIView(ListCreateAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer


# Slider GET & PUT & PATCH & DELETE
class SliderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer


# FAQ GET & POST
class FAQListCreateAPIView(ListCreateAPIView):
    # queryset = FAQ.objects.filter(is_active=True).all()
    queryset = FAQ.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = InfiniteScrollPagination
    filterset_fields = ['is_active']
    search_fields = ['faq']
    serializer_class = FAQSerializer


# FAQ GET & PUT & PATCH & DELETE
class FAQRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.filter(is_active=True).all()
    serializer_class = FAQSerializer
