from django.conf import settings
from django.utils import timezone
from django.db.models import Count
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from ..utils.otp import generate_otp
from ..models import User, OTPToken, Subscription
from ..serializers import (
    LoginTokenSerializer,
    PopularChannelSerializer,
    RegisterSerializer,
    VerifyOTPSerializer,
    ResendOTPSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
    SubscriptionReadWebSerializer,
    UserDetailSerializer
)
from services.pagination import InfiniteScrollPagination


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

        try:
            otp_token = OTPToken.objects.get(
                user__email=email, otp_code=otp_code)
        except OTPToken.DoesNotExist:
            return Response(data={"message": 'Invalid email or OTP code.'}, status=status.HTTP_400_BAD_REQUEST)

        if otp_token.otp_expires_at is not None and otp_token.otp_expires_at < timezone.now():
            return Response(data={"message": 'OTP has expired. Please request a new one.'}, status=status.HTTP_403_FORBIDDEN)

        if not otp_token.is_verified:
            otp_token.is_verified = True
            otp_token.save()

            otp_token.user.is_active = True
            otp_token.user.status = 'Active'
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
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

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


class ChangePasswordAPIView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer


class SubscribeWebAPIView(ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionReadWebSerializer
    pagination_class = InfiniteScrollPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(follower=self.request.user)


class ToggleSubscribeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'delete']

    def post(self, request, pk, *args, **kwargs):
        follower = request.user
        follows = get_object_or_404(User, pk=pk)

        if follower == follows:
            return Response({'error': 'You cannot subscribe to yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        subscription, created = Subscription.objects.get_or_create(
            follower=follower, follows=follows)

        return Response({'status': 'subscribed'}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, *args, **kwargs):
        follower = request.user
        follows = get_object_or_404(User, pk=pk)
        try:
            subscription = Subscription.objects.get(
                follower=follower, follows=follows)
            subscription.delete()
            return Response({'status': 'unsubscribed'}, status=status.HTTP_204_NO_CONTENT)
        except Subscription.DoesNotExist:
            return Response({'error': 'Subscription does not exist'}, status=status.HTTP_404_NOT_FOUND)


class PopularChannelsAPIView(APIView):

    def get(self, request, *args, **kwargs):
        popular_channels = User.objects.annotate(
            followers_count=Count('followers')
        ).order_by('-followers_count')[:5]

        serializer = PopularChannelSerializer(popular_channels, many=True)
        return Response(serializer.data)


class SubscriptionsAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = PopularChannelSerializer
    filter_backends = [OrderingFilter]
    pagination_class = InfiniteScrollPagination

    def get_queryset(self):
        subscriptions = User.objects.annotate(
            followers_count=Count('followers')
        )
        subscriptions = subscriptions[:50]
        return subscriptions


class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
