from django.urls import path
from .views import WishlistAPIView, BasketAPIView

urlpatterns = [
    path('basket/', BasketAPIView.as_view(), name='api-basket'),
    path('wishlist/', WishlistAPIView.as_view(), name = "wishlists"),
]