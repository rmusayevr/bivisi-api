from django.urls import path
from .views.web_views import WishlistAPIView, BasketAPIView
from .views.admin_views import (
    WishlistListCreateAPIView,
    WishlistRetrieveUpdateDestroyAPIView,
    BasketItemListCreateAPIView,
    BasketItemRetrieveUpdateDestroyAPIView,
    BasketListCreateAPIView,
    BasketRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('basket/', BasketAPIView.as_view(), name='api-basket'),
    path('wishlist/', WishlistAPIView.as_view(), name="wishlists"),


    # Wishlist URLs
    path('admin/wishlist/', WishlistListCreateAPIView.as_view(),
         name='wishlist_list_create'),
    path('admin/wishlist/<int:pk>/',
         WishlistRetrieveUpdateDestroyAPIView.as_view(), name='wishlist_detail'),

    # Basket Item URLs
    path('admin/basket_item/', BasketItemListCreateAPIView.as_view(),
         name='basket_item_list_create'),
    path('admin/basket_item/<int:pk>/',
         BasketItemRetrieveUpdateDestroyAPIView.as_view(), name='basket_item_detail'),

    # Basket URLs
    path('admin/basket/', BasketListCreateAPIView.as_view(),
         name='basket_list_create'),
    path('admin/basket/<int:pk>/',
         BasketRetrieveUpdateDestroyAPIView.as_view(), name='basket_detail'),
]
