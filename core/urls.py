from django.urls import path
from .views import SliderListCreateAPIView, SliderRetrieveUpdateDestroyAPIView


urlpatterns = [

    # Project All Image URLs
    path('slider/', SliderListCreateAPIView.as_view(), name='slider_list_create'),
    path('slider/<int:pk>/', SliderRetrieveUpdateDestroyAPIView.as_view(), name='slider_detail'),

]
