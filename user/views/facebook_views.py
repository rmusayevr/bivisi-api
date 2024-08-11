import random
import string
import requests
from django.core.files.base import ContentFile
from django.contrib.auth import login
from django.conf import settings
from django.utils.text import slugify
from django.shortcuts import redirect
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from ..service import FacebookLoginFlowService


class PublicApi(APIView):
    authentication_classes = ()
    permission_classes = ()


class FacebookLoginRedirectApi(PublicApi):
    def get(self, request, *args, **kwargs):
        facebook_login_flow = FacebookLoginFlowService()
        authorization_url, state = facebook_login_flow.get_authorization_url()

        request.session["facebook_oauth2_state"] = state
        return redirect(authorization_url)


class FacebookLoginApi(PublicApi):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)
        state = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        code = validated_data.get("code")
        error = validated_data.get("error")
        state = validated_data.get("state")

        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        if not code or not state:
            return Response({"error": "Code and state are required."}, status=status.HTTP_400_BAD_REQUEST)

        session_state = request.session.get("facebook_oauth2_state")

        if session_state is None:
            return Response({"error": "CSRF check failed."}, status=status.HTTP_400_BAD_REQUEST)

        del request.session["facebook_oauth2_state"]

        if state != session_state:
            return Response({"error": "CSRF check failed."}, status=status.HTTP_400_BAD_REQUEST)

        facebook_login_flow = FacebookLoginFlowService()
        tokens = facebook_login_flow.get_tokens(code=code)
        access_token = tokens.get("access_token")
        user_info = facebook_login_flow.get_user_info(
            access_token=access_token)

        user_email = user_info.get("email")

        User = get_user_model()
        user, created = User.objects.get_or_create(email=user_email)

        if created:
            user.first_name = user_info.get("name", "").split()[0]
            user.last_name = " ".join(user_info.get("name", "").split()[1:])
            user.username = self.generate_unique_username(user_email)
            profile_image_url = user_info.get("picture", {}).get("data", {}).get("url")

            if profile_image_url:
                self.save_profile_image(user, profile_image_url)

            user.is_active = True
            user.status = "Active"
            user.sign_up_method = "facebook"
            user.save()

        login(request, user)

        result = {
            "user_info": user_info,
            "access_token": access_token,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "username": user.username,
        }

        return redirect(f"{settings.BASE_FRONTEND_URL}", {"result": result})

    def generate_unique_username(self, email):
        base_username = slugify(email.split('@')[0])
        username = base_username
        User = get_user_model()
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}"
        return username

    def save_profile_image(self, user, image_url):
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            filename = slugify(user.username) + ".jpg"
            user.avatar.save(filename, ContentFile(
                response.content), save=False)
        except requests.exceptions.RequestException as e:
            return f"Error downloading or saving profile image for user {user.username}: {e}"
