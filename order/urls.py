from django.urls import path
from .views.web_views import (
    FavoriteWebAPIView,
    ToggleFavoriteAPIView,
    AddBasketAPIView,
    ChangeBasketItemAPIView,
    DeleteBasketItemAPIView,
    DeleteBasketAPIView,
    BasketWebAPIView
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
    # Favorite Admin URLs
    path('admin/favorites/', FavoriteListCreateAPIView.as_view(),
         name='favorite_list_create'),
    path('admin/favorite/<int:pk>/',
         FavoriteRetrieveUpdateDestroyAPIView.as_view(), name='favorite_detail'),

    # Favorite Web URLs
    path('favorites/', FavoriteWebAPIView.as_view(),
         name='favorite_list'),
    path('toggle_favorite/<int:pk>/',
         ToggleFavoriteAPIView.as_view(), name='toggle_favorite'),

    # Basket Item URLs
    path('admin/basket_item/', BasketItemListCreateAPIView.as_view(),
         name='basket_item_list_create'),
    path('admin/basket_item/<int:pk>/',
         BasketItemRetrieveUpdateDestroyAPIView.as_view(), name='basket_item_detail'),

    # Basket Admin URLs
    path('admin/basket/', BasketListCreateAPIView.as_view(),
         name='basket_list_create'),
    path('admin/basket/<int:pk>/',
         BasketRetrieveUpdateDestroyAPIView.as_view(), name='basket_detail'),

    # Basket Web URLs
    path('basket/', BasketWebAPIView.as_view(), name='basket_list'),
    path('add_basket_item/<int:pk>/',
         AddBasketAPIView.as_view(), name='add_basket_item'),
    path('change_basket_item/<int:pk>/',
         ChangeBasketItemAPIView.as_view(), name='change_basket_item'),
    path('delete_basket_item/<int:pk>/',
         DeleteBasketItemAPIView.as_view(), name='delete_basket_item'),
    path('delete_basket/', DeleteBasketAPIView.as_view(), name='delete_basket'),
]
