from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status


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

    def get_response(self):
        # Get the user
        user = self.user

        # Prepare the response data
        data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

        # Return a custom response with user details
        return Response(data, status=status.HTTP_200_OK)