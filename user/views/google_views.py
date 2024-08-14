from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings
from django.core.files.base import ContentFile
from dj_rest_auth.registration.views import SocialLoginView
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken  # For generating tokens


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.BASE_FRONTEND_URL
    client_class = OAuth2Client

    def process_login(self):
        # Call the original process_login method
        super().process_login()

        # Get the user
        user = self.user

        if not user.is_active:
            # Update the user status and sign_up_method only if the user is newly registered
            user.status = "Active"
            user.is_active = True
            user.sign_up_method = "google"
            user.save()

        # Save Google profile picture as avatar
        social_account = user.socialaccount_set.filter(provider='google').first()
        if social_account:
            google_data = social_account.extra_data
            profile_picture_url = google_data.get('picture')
            if profile_picture_url:
                avatar_response = requests.get(profile_picture_url)
                if avatar_response.status_code == 200:
                    # Save the image to the user's avatar field
                    user.avatar.save(
                        f'{user.username}_avatar.jpg',
                        ContentFile(avatar_response.content),
                        save=True
                    )

    def get_response(self):
        # Get the user
        user = self.user

        # Generate the access and refresh tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Prepare the response data
        data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'status': user.status,
            'access': access_token,
            'refresh': refresh_token,
        }

        # Return a custom response with user details
        return Response(data, status=status.HTTP_200_OK)