from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.BASE_FRONTEND_URL
    client_class = OAuth2Client

    def process_login(self):
        # Call the original process_login method
        super().process_login()

        # Get the user
        user = self.user

        # Update the user status and sign_up_method
        user.status = "Active"
        user.is_active = True
        user.sign_up_method = "google"
        user.save()
