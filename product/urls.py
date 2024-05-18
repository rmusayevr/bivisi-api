from django.urls import path
from product.views.web_views.product_comment import ParentCommentListAPIView, SubCommentListAPIView
from .views.web_views.product import WebProductVideoTypeListView
from .views.web_views.product_and_comment_like import ToggleProductCommentLikeAPIView, ToggleProductLikeAPIView
from .views.web_views.history import UserProductHistoryReadAPIView, UserProductHistoryCreateAPIView
from .views.admin_views.views import (CategoryListCreateAPIView,
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

    # User Product Like URLs
    path('user_product_like/', UserProductLikeListCreateAPIView.as_view(),
         name='user_product_like_list_create'),
    path('user_product_like/<int:pk>/',
         UserProductLikeRetrieveUpdateDestroyAPIView.as_view(), name='user_product_like_detail'),

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
    path('sub_comments/<int:product_id>/<int:parent_comment_id>/',
         SubCommentListAPIView.as_view(), name='sub_comments'),


    # User Product History
#     path('history/', UserProductHistoryReadAPIView.as_view(),
#          name='user_product_views'),
#     path('add_history/<int:product_id>/',
#          UserProductHistoryCreateAPIView.as_view(), name='create_user_product_views')

]
