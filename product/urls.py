from django.urls import path
from product.views.web_views.product_comment import (
    ParentCommentListAPIView,
    ProductCommentCreateView,
    ProductCommentDeleteView,
    SubCommentListAPIView
)
from .views.web_views.product import (
    ChannelWebProductTypeListView,
    ShortsDeleteAPIView,
    TrendingAPIView,
    UpdateProductPremiumView,
    WebProductDeleteAPIView,
    WebProductVideoTypeListView,
    WebUploadProductCreateView,
    UserProductLikeWebAPIView,
    UserWebProductTypeListView,
    WebUploadProductUpdateView
)
from .views.web_views.product_and_comment_like import (
    ToggleProductCommentLikeAPIView,
    ToggleProductLikeAPIView
)
from .views.web_views.category import CategoryWebListView
from .views.admin_views.views import (
    CategoryListCreateAPIView,
    CategoryRetrieveUpdateDestroyAPIView,
    DashboardProductVideoTypeListCreateAPIView,
    DashboardProductVideoTypeRetrieveUpdateDestroyAPIView,
    ProductCommentLikeListCreateAPIView,
    ProductCommentLikeRetrieveUpdateDestroyAPIView,
    ProductCommentListCreateAPIView,
    ProductCommentRetrieveUpdateDestroyAPIView,
    ProductListCreateAPIView,
    ProductRetrieveUpdateDestroyAPIView,
    UserProductLikeListCreateAPIView,
    UserProductLikeRetrieveUpdateDestroyAPIView,
)


urlpatterns = [
    # Category URLs
    path('category/', CategoryListCreateAPIView.as_view(),
         name='category_list_create'),
    path('category/<int:pk>/',
         CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category_detail'),

    path('categories/', CategoryWebListView.as_view(), name='category_list'),

    # Product URLs
    path('product/', ProductListCreateAPIView.as_view(),
         name='product_list_create'),
    path('product/<int:pk>/',
         ProductRetrieveUpdateDestroyAPIView.as_view(), name='product_detail'),

    # Dashboard Product Video Type URLs
    path('dashboard_product_video_type/', DashboardProductVideoTypeListCreateAPIView.as_view(),
         name='dashboard_product_video_type_list_create'),
    path('dashboard_product_video_type/<int:pk>/',
         DashboardProductVideoTypeRetrieveUpdateDestroyAPIView.as_view(), name='dashboard_product_video_type_detail'),

    # Web Product Video Type URLs
    path('web_products/', WebProductVideoTypeListView.as_view(),
         name='web_products_list'),

    path('user_web_products/', UserWebProductTypeListView.as_view(),
         name='user_web_products'),
    path('channel_web_products/<str:username>/',
         ChannelWebProductTypeListView.as_view(), name='channel_products'),

    # User Product Like URLs
    path('user_product_like/', UserProductLikeListCreateAPIView.as_view(),
         name='user_product_like_list_create'),
    path('user_product_like/<int:pk>/',
         UserProductLikeRetrieveUpdateDestroyAPIView.as_view(), name='user_product_like_detail'),

    path('liked_products/', UserProductLikeWebAPIView.as_view(),
         name='liked_products'),

    # Product Comment URLs
    path('product_comment/', ProductCommentListCreateAPIView.as_view(),
         name='product_comment_list_create'),
    path('product_comment/<int:pk>/',
         ProductCommentRetrieveUpdateDestroyAPIView.as_view(), name='product_comment_detail'),

    # Product Comment Like  URLs
    path('product_comment_like/', ProductCommentLikeListCreateAPIView.as_view(),
         name='product_comment_like_list_create'),
    path('product_comment_like/<int:pk>/',
         ProductCommentLikeRetrieveUpdateDestroyAPIView.as_view(), name='product_comment_like_detail'),

    # Product Like
    path('toggle_product_like/<int:product_id>/',
         ToggleProductLikeAPIView.as_view(), name='toggle_product_like'),

    # Product Like
    path('toggle_product_comment_like/<int:product_comment_id>/',
         ToggleProductCommentLikeAPIView.as_view(), name='toggle_product_comment_like'),

    # Parent and Sub Comments
    path('parent_comments/<int:product_id>/',
         ParentCommentListAPIView.as_view(), name='parent_comments'),
    path('sub_comments/<int:parent_comment_id>/',
         SubCommentListAPIView.as_view(), name='sub_comments'),

    path('create_comment/', ProductCommentCreateView.as_view(),
         name='create_comment'),

    path('delete_comment/<int:pk>/', ProductCommentDeleteView.as_view(),
         name='delete_comment'),

    path('upload_product/', WebUploadProductCreateView.as_view(),
         name='upload_product'),
    path('update_product/<int:pk>/<int:product_type_id>/',
         WebUploadProductUpdateView.as_view(), name='update_product'),
    path('product_delete/<int:pk>/',
         WebProductDeleteAPIView.as_view(), name='product_delete'),
    path('product_shorts_delete/<int:pk>/',
         ShortsDeleteAPIView.as_view(), name='product_shorts_delete'),

    path('update_premium_products/', UpdateProductPremiumView.as_view(),
         name='update-premium-products'),

    path('trending_videos/', TrendingAPIView.as_view(),
         name='trending_videos'),



]
