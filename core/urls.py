from django.urls import path
from .views import FAQListCreateAPIView, FAQRetrieveUpdateDestroyAPIView, SliderListCreateAPIView, SliderRetrieveUpdateDestroyAPIView


urlpatterns = [

    # FAQ URLs
    path('faq/', FAQListCreateAPIView.as_view(), name='faq_list_create'),
    path('faq/<int:pk>/', FAQRetrieveUpdateDestroyAPIView.as_view(), name='faq_detail'),

    # Project All Image URLs
    path('slider/', SliderListCreateAPIView.as_view(), name='slider_list_create'),
    path('slider/<int:pk>/', SliderRetrieveUpdateDestroyAPIView.as_view(), name='slider_detail'),

]
