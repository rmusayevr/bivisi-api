from django.urls import path
from .views.web_views import (
    ToggleFavoriteAPIView,
    AddBasketAPIView,
    DeleteBasketItemAPIView,
    DeleteBasketAPIView,
)
from .views.admin_views import (
    FavoriteListCreateAPIView,
    FavoriteRetrieveUpdateDestroyAPIView,
    BasketItemListCreateAPIView,
    BasketItemRetrieveUpdateDestroyAPIView,
    BasketListCreateAPIView,
    BasketRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    # Favorite URLs
    path('favorites/', FavoriteListCreateAPIView.as_view(),
         name='favorite_list_create'),
    path('favorite/<int:pk>/',
         FavoriteRetrieveUpdateDestroyAPIView.as_view(), name='favorite_detail'),
    path('toggle_favorite/<int:pk>/',
         ToggleFavoriteAPIView.as_view(), name='toggle_favorite'),

    # Basket Item URLs
    path('basket_item/', BasketItemListCreateAPIView.as_view(),
         name='basket_item_list_create'),
    path('basket_item/<int:pk>/',
         BasketItemRetrieveUpdateDestroyAPIView.as_view(), name='basket_item_detail'),

    # Basket URLs
    path('basket/', BasketListCreateAPIView.as_view(),
         name='basket_list_create'),
    path('basket/<int:pk>/',
         BasketRetrieveUpdateDestroyAPIView.as_view(), name='basket_detail'),
    path('add_basket_item/<int:pk>/',
         AddBasketAPIView.as_view(), name='toggle_basket_item'),
    path('delete_basket_item/<int:pk>/',
         DeleteBasketItemAPIView.as_view(), name='delete_basket_item'),
    path('delete_basket/', DeleteBasketAPIView.as_view(), name='delete_basket'),
]
