from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from ..utils.otp import generate_otp
from ..models import User, OTPToken
from ..serializers import (
    LoginTokenSerializer,
    ResendOTPSerializer,
    ResetPasswordSerializer,
)


class SendEmailResetPasswordAPIView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ResendOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

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
                                http://157.230.120.254/user/verify-otp

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
        return Response({'message': 'Reset Password OTP has been sent.'})


class ResetPasswordAPIView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data['new_password']
        email = serializer.validated_data["email"]
        otp_code = serializer.validated_data["otp_code"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'Invalid reset request.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            last_otp_token = OTPToken.objects.filter(
                user__email=email, otp_code=otp_code).latest('tp_created_at')
            if not last_otp_token.is_verified:
                return Response({'message': 'OTP not verified.'}, status=status.HTTP_400_BAD_REQUEST)
        except OTPToken.DoesNotExist:
            return Response({'message': 'No OTP token found.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        login_user = authenticate(
            request, username=email, password=new_password)
        if login_user is not None:
            login(request, user)
            refresh = LoginTokenSerializer.get_token(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'email': user.email
            }
            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response({'message': 'Password reset successfully but login failed.'}, status=status.HTTP_400_BAD_REQUEST)
