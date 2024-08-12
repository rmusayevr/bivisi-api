from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

    def process_login(self):
        # Call the original process_login method
        super().process_login()

        # Get the user
        user = self.user

        # Update the user status and sign_up_method
        user.status = "Active"
        user.is_active = True
        user.sign_up_method = "facebook"
        user.save()