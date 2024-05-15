from django.urls import path
from .views.web_views import (
    PopularChannelsAPIView,
    RegisterAPIView,
    LoginTokenView,
    OTPVerifyAPIView,
    OTPResendAPIView,
    SendEmailResetPasswordAPIView,
    ResetPasswordAPIView,
    ChangePasswordAPIView,
    ToggleSubscribeAPIView
)
from .views.admin_views import (
    SubscriptionListCreateAPIView,
    SubscriptionRetrieveUpdateDestroyAPIView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('login/', LoginTokenView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', RegisterAPIView.as_view(), name='register'),
    path('verify_otp/', OTPVerifyAPIView.as_view(), name='verify-otp'),
    path('resend_otp/', OTPResendAPIView.as_view(), name='resend-otp'),

    path('send_email_reset_password/', SendEmailResetPasswordAPIView.as_view(),
         name='send-email-reset-password'),
    path('reset_password/', ResetPasswordAPIView.as_view(),
         name='reset-password'),
    path('change_password/<int:pk>/', ChangePasswordAPIView.as_view(),
         name='change-password'),

    path('subscription/', SubscriptionListCreateAPIView.as_view(),
         name='subscription_list_create'),
    path('subscription/<int:pk>/', SubscriptionRetrieveUpdateDestroyAPIView.as_view(),
         name='subscription_detail'),
    path('toggle_subscribe/<int:pk>/',
         ToggleSubscribeAPIView.as_view(), name='toggle_subscribe'),

    path('popular-channels/', PopularChannelsAPIView.as_view(),
         name='popular_channels'),

]
