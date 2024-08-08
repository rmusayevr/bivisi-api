from django.urls import path

from user.views.otp_views import (
    OTPResendAPIView,
    OTPVerifyAPIView
)
from user.views.profile_settings import (
    GeneralSettingsUpdateView,
    ProfileInformationUpdateView
)
from user.views.reset_password import (
    ResetPasswordAPIView,
    SendEmailResetPasswordAPIView
)
from user.views.subscription import (
    PopularChannelsAPIView,
    SubscribeWebAPIView,
    SubscriptionsAPIView,
    ToggleSubscribeAPIView
)
from .views.web_views import (
    RegisterAPIView,
    LoginTokenView,
    ChangePasswordAPIView,
    UpdateTokenView,
    UserDetailAPIView,
    UserListAPIView,
    DeleteAccountAPIView
)
from .views.admin_views import (
    ChannelCategoryListCreateAPIView,
    ChannelCategoryRetrieveUpdateDestroyAPIView,
    PhoneNumberListCreateAPIView,
    PhoneNumberRetrieveUpdateDestroyAPIView,
    SubscriptionListCreateAPIView,
    SubscriptionRetrieveUpdateDestroyAPIView,
)
from .views.google_views import (
    GoogleLoginApi,
    GoogleLoginRedirectApi,
)
from .views.facebook_views import (
    FacebookLoginApi,
    FacebookLoginRedirectApi,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("google/callback/", GoogleLoginApi.as_view(), name="callback-raw"),
    path("google/redirect/", GoogleLoginRedirectApi.as_view(), name="redirect-raw"),

    path("facebook/callback/", FacebookLoginApi.as_view(),
         name="callback-facebook"),
    path("facebook/redirect/", FacebookLoginRedirectApi.as_view(),
         name="redirect-facebook"),

    path('login/', LoginTokenView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('update-token/', UpdateTokenView.as_view(), name='update_token'),

    path('register/', RegisterAPIView.as_view(), name='register'),
    path('verify_otp/', OTPVerifyAPIView.as_view(), name='verify-otp'),
    path('resend_otp/', OTPResendAPIView.as_view(), name='resend-otp'),

    path('send_email_reset_password/', SendEmailResetPasswordAPIView.as_view(),
         name='send-email-reset-password'),
    path('reset_password/', ResetPasswordAPIView.as_view(),
         name='reset-password'),
    path('change_password/<int:pk>/', ChangePasswordAPIView.as_view(),
         name='change-password'),

    path('your_subscribers/', SubscribeWebAPIView.as_view(),
         name='subscriber_list'),
    path('subscriptions/', SubscriptionsAPIView.as_view(),
         name='subscriber_list'),
    path('toggle_subscribe/<int:pk>/',
         ToggleSubscribeAPIView.as_view(), name='toggle_subscribe'),

    path('popular-channels/', PopularChannelsAPIView.as_view(),
         name='popular_channels'),

    path('general_settings/', GeneralSettingsUpdateView.as_view(),
         name='general_settings'),

    path('profile_information/', ProfileInformationUpdateView.as_view(),
         name='profile_information'),

    path('user_detail/', UserDetailAPIView.as_view(), name='user_detail'),
    path('users/', UserListAPIView.as_view(), name='users'),

    path('delete_account/', DeleteAccountAPIView.as_view(), name='delete_account'),

]

urlpatterns += [
    path('admin/subscription/', SubscriptionListCreateAPIView.as_view(),
         name='subscription_list_create'),
    path('admin/subscription/<int:pk>/', SubscriptionRetrieveUpdateDestroyAPIView.as_view(),
         name='subscription_detail'),

    path('admin/phone_number/', PhoneNumberListCreateAPIView.as_view(),
         name='phone_number_list_create'),
    path('admin/phone_number/<int:pk>/', PhoneNumberRetrieveUpdateDestroyAPIView.as_view(),
         name='phone_number_detail'),

    path('admin/channel_category/', ChannelCategoryListCreateAPIView.as_view(),
         name='channel_category_list_create'),
    path('admin/channel_category/<int:pk>/', ChannelCategoryRetrieveUpdateDestroyAPIView.as_view(),
         name='channel_category_detail'),
]
