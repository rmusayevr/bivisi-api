from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView
from ..utils.otp import generate_otp
from ..models import User, OTPToken
from ..serializers import (
    LoginTokenSerializer,
    RegisterSerializer,
    VerifyOTPSerializer,
    ResendOTPSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer
)
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone
from django.core.mail import send_mail


class LoginTokenView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginTokenSerializer


class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class OTPVerifyAPIView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = VerifyOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']

        otp_token = OTPToken.objects.get(
            user__email=email, otp_code=otp_code)

        if otp_token.otp_expires_at is not None and otp_token.otp_expires_at < timezone.now():
            return Response(data={"message": 'OTP has expired. Please request a new one.'}, status=status.HTTP_403_FORBIDDEN)

        if not otp_token.is_verified:
            otp_token.is_verified = True
            otp_token.save()

            otp_token.user.is_active = True
            otp_token.user.save()

            return Response({'message': 'OTP verification successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'OTP already verified.'}, status=status.HTTP_400_BAD_REQUEST)


class OTPResendAPIView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ResendOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        try:
            otp_token = OTPToken.objects.get(user=user)
        except ObjectDoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        new_otp_code = generate_otp(user.id)

        otp_token.otp_code = new_otp_code
        otp_token.otp_expires_at = timezone.now() + timezone.timedelta(minutes=2)
        otp_token.save()

        subject = "Email Verification"
        message = f"""
                                Hi {user.username}, here is your OTP {otp_token.otp_code}
                                it expires in 2 minute, use the url below to redirect back to the website
                                http://localhost:5173/user/verify-otp

                                """
        sender = settings.AUTH_USER_MODEL
        receiver = [email, ]

        send_mail(
            subject,
            message,
            sender,
            receiver,
            fail_silently=False,
        )
        return Response({'message': 'New OTP code has been sent.'})


class SendEmailResetPasswordAPIView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ResendOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        try:
            otp_token = OTPToken.objects.get(user=user)
            otp_token.is_verified = False
            otp_token.save()
        except ObjectDoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        new_otp_code = generate_otp(user.id)

        otp_token.otp_code = new_otp_code
        otp_token.otp_expires_at = timezone.now() + timezone.timedelta(minutes=2)
        otp_token.save()

        subject = "Email Verification"
        message = f"""
                                Hi {user.username}, here is your OTP {otp_token.otp_code}
                                it expires in 2 minute, use the url below to redirect back to the website
                                http://localhost:5173/user/verify-otp

                                """
        sender = settings.AUTH_USER_MODEL
        receiver = [email, ]

        send_mail(
            subject,
            message,
            sender,
            receiver,
            fail_silently=False,
        )
        return Response({'message': 'Reset Password Link has been sent.'})


class ResetPasswordAPIView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data['new_password']
        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'Invalid reset request.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            last_otp_token = OTPToken.objects.filter(
                user=user).latest('tp_created_at')
            if not last_otp_token.is_verified:
                return Response({'message': 'OTP not verified.'}, status=status.HTTP_400_BAD_REQUEST)
        except OTPToken.DoesNotExist:
            return Response({'message': 'No OTP token found.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)


class ChangePasswordAPIView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = ChangePasswordSerializer
