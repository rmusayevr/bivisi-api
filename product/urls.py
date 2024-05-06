from django.urls import path
from .views import (
    CategoryListCreateAPIView,
    CategoryRetrieveUpdateDestroyAPIView,
    ProductCommentListCreateAPIView,
    ProductCommentRetrieveUpdateDestroyAPIView,
    ProductListCreateAPIView,
    ProductRetrieveUpdateDestroyAPIView,
    UserProductLikeListCreateAPIView,
    UserProductLikeRetrieveUpdateDestroyAPIView,
)



urlpatterns = [
    # Category URLs
    path('category/', CategoryListCreateAPIView.as_view(), name='category_list_create'),
    path('category/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category_detail'),

    # Product URLs
    path('product/', ProductListCreateAPIView.as_view(), name='product_list_create'),
    path('product/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product_detail'),

    # User Product Like URLs
    path('user_product_like/', UserProductLikeListCreateAPIView.as_view(), name='user_product_like_list_create'),
    path('user_product_like/<int:pk>/', UserProductLikeRetrieveUpdateDestroyAPIView.as_view(), name='user_product_like_detail'),

    # Product Comment URLs
    path('product_comment/', ProductCommentListCreateAPIView.as_view(), name='product_comment_list_create'),
    path('product_comment/<int:pk>/', ProductCommentRetrieveUpdateDestroyAPIView.as_view(), name='product_comment_detail'),

    # Product Comment Like  URLs
    path('user_product_like/', UserProductLikeListCreateAPIView.as_view(), name='user_product_like_list_create'),
    path('user_product_like/<int:pk>/', UserProductLikeRetrieveUpdateDestroyAPIView.as_view(), name='user_product_like_detail'),

]
