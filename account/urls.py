from django.urls import path
from .views import (
    RegisterAPIView,
    LoginTokenView,
    OTPVerifyAPIView,
    OTPResendAPIView,
    SendEmailResetPasswordAPIView
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('login/', LoginTokenView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', RegisterAPIView.as_view(), name='register'),
    path('verify-otp/', OTPVerifyAPIView.as_view(), name='verify-otp'),
    path('resend-otp/', OTPResendAPIView.as_view(), name='resend-otp'),

    path('reset-password/', SendEmailResetPasswordAPIView.as_view(),
         name='reset-password'),
]
