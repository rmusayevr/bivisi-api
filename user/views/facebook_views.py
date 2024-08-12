from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken  # For generating tokens
import requests
from django.core.files.base import ContentFile


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

    def process_login(self):
        # Call the original process_login method
        super().process_login()

        # Get the user
        user = self.user

        if not user.is_active:
            # Update the user status and sign_up_method only if the user is newly registered
            user.status = "Active"
            user.is_active = True
            user.sign_up_method = "facebook"
            user.save()

        # Save Facebook profile picture as avatar
        social_account = user.socialaccount_set.filter(provider='facebook').first()
        if social_account:
            facebook_data = social_account.extra_data
            user_id = facebook_data.get('id')
            if user_id:
                # Request the profile picture using Facebook Graph API
                profile_picture_url = f'https://graph.facebook.com/{user_id}/picture?type=large'
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
            'access_token': access_token,
            'refresh_token': refresh_token,
        }

        # Prepare the response data
        data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

        # Return a custom response with user details
        return Response(data, status=status.HTTP_200_OK)
