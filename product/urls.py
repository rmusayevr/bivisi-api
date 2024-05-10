from django.urls import path
from .views import (CategoryListCreateAPIView,
                    CategoryRetrieveUpdateDestroyAPIView,
                    ProductCommentLikeListCreateAPIView,
                    ProductCommentLikeRetrieveUpdateDestroyAPIView,
                    ProductCommentListCreateAPIView,
                    ProductCommentRetrieveUpdateDestroyAPIView,
                    ProductListCreateAPIView,
                    ProductRetrieveUpdateDestroyAPIView,
                    ProductVideoTypeListCreateAPIView,
                    ProductVideoTypeRetrieveUpdateDestroyAPIView,
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

    # Product Video Type URLs
    path('product_video_type/', ProductVideoTypeListCreateAPIView.as_view(), name='product_video_type_list_create'),
    path('product_video_type/<int:pk>/', ProductVideoTypeRetrieveUpdateDestroyAPIView.as_view(), name='product_video_type_detail'),

    # User Product Like URLs
    path('user_product_like/', UserProductLikeListCreateAPIView.as_view(), name='user_product_like_list_create'),
    path('user_product_like/<int:pk>/', UserProductLikeRetrieveUpdateDestroyAPIView.as_view(), name='user_product_like_detail'),

    # Product Comment URLs
    path('product_comment/', ProductCommentListCreateAPIView.as_view(), name='product_comment_list_create'),
    path('product_comment/<int:pk>/', ProductCommentRetrieveUpdateDestroyAPIView.as_view(), name='product_comment_detail'),

    # Product Comment Like  URLs
    path('product_comment_like/', ProductCommentLikeListCreateAPIView.as_view(), name='product_comment_like_list_create'),
    path('product_comment_like/<int:pk>/', ProductCommentLikeRetrieveUpdateDestroyAPIView.as_view(), name='product_comment_like_detail'),

]
