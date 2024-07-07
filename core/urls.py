from django.urls import path
from .views import (
    FAQListCreateAPIView,
    FAQRetrieveUpdateDestroyAPIView,
    SliderListCreateAPIView,
    SliderRetrieveUpdateDestroyAPIView,
    StreamListCreateAPIView,
    StreamRetrieveUpdateDestroyAPIView
)


urlpatterns = [

    # FAQ URLs
    path('faq/', FAQListCreateAPIView.as_view(), name='faq_list_create'),
    path('faq/<int:pk>/', FAQRetrieveUpdateDestroyAPIView.as_view(), name='faq_detail'),

    # Project All Image URLs
    path('slider/', SliderListCreateAPIView.as_view(), name='slider_list_create'),
    path('slider/<int:pk>/', SliderRetrieveUpdateDestroyAPIView.as_view(),
         name='slider_detail'),

    # FAQ URLs
    path('stream/', StreamListCreateAPIView.as_view(), name='stream_list_create'),
    path('stream/delete/<str:room_id>/',
         StreamRetrieveUpdateDestroyAPIView.as_view(), name='stream_delete'),

]
