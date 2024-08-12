# import json
# import random
# import string
# import requests
# from django.core.files.base import ContentFile
# from django.conf import settings
# from django.contrib.auth import login
# from django.http import HttpResponseRedirect, JsonResponse
# from django.utils.text import slugify
# from django.shortcuts import redirect
# from rest_framework import serializers, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.tokens import RefreshToken

# from ..service import GoogleRawLoginFlowService


# class PublicApi(APIView):
#     authentication_classes = ()
#     permission_classes = ()


# class GoogleLoginRedirectApi(PublicApi):
#     def get(self, request, *args, **kwargs):
#         google_login_flow = GoogleRawLoginFlowService()

#         authorization_url, state = google_login_flow.get_authorization_url()

#         request.session["google_oauth2_state"] = state

#         return redirect(authorization_url)


# class GoogleLoginApi(PublicApi):
#     class InputSerializer(serializers.Serializer):
#         code = serializers.CharField(required=False)
#         error = serializers.CharField(required=False)
#         state = serializers.CharField(required=False)

#     def get(self, request, *args, **kwargs):
#         input_serializer = self.InputSerializer(data=request.GET)
#         input_serializer.is_valid(raise_exception=True)

#         validated_data = input_serializer.validated_data

#         code = validated_data.get("code")
#         error = validated_data.get("error")
#         state = validated_data.get("state")

#         if error is not None:
#             return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

#         if code is None or state is None:
#             return Response({"error": "Code and state are required."}, status=status.HTTP_400_BAD_REQUEST)

#         session_state = request.session.get("google_oauth2_state")

#         if session_state is None:
#             return Response({"error": "CSRF check failed."}, status=status.HTTP_400_BAD_REQUEST)

#         del request.session["google_oauth2_state"]

#         if state != session_state:
#             return Response({"error": "CSRF check failed."}, status=status.HTTP_400_BAD_REQUEST)

#         google_login_flow = GoogleRawLoginFlowService()

#         google_tokens = google_login_flow.get_tokens(code=code)

#         id_token_decoded = google_tokens.decode_id_token()
#         user_info = google_login_flow.get_user_info(google_tokens=google_tokens)

#         user_email = id_token_decoded["email"]

#         User = get_user_model()  # Get the user model dynamically
#         user, created = User.objects.get_or_create(email=user_email)

#         if created:
#             # Extract or generate required fields
#             user.first_name = user_info.get("given_name", "")
#             user.last_name = user_info.get("family_name", "")
#             user.username = self.generate_unique_username(user_email)
#             profile_image_url = user_info.get("picture")

#             if profile_image_url:
#                 self.save_profile_image(user, profile_image_url)

#             user.is_active = True
#             user.status = "Active"
#             user.sign_up_method = "google"
#             user.save()

#         login(request, user)

#         # Generate JWT token
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)

#         # Store data in a secure, HTTP-only cookie
#         data = {
#             'access_token': access_token,
#             'username': user.username,
#             'email': user.email,
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#         }

#         return JsonResponse(data)

#     def generate_unique_username(self, email):
#         base_username = slugify(email.split('@')[0])
#         username = base_username
#         User = get_user_model()
#         # Ensure the username is unique
#         while User.objects.filter(username=username).exists():
#             # Append a random string if the username is taken
#             username = f"{base_username}{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}"

#         return username

#     def save_profile_image(self, user, image_url):
#         try:
#             response = requests.get(image_url)
#             response.raise_for_status()  # Ensure the request was successful

#             # Generate a filename
#             filename = slugify(user.username) + ".jpg"

#             # Save the image to the avatar field
#             user.avatar.save(filename, ContentFile(
#                 response.content), save=False)
#         except requests.exceptions.RequestException as e:
#             # Handle potential errors with image downloading
#             return f"Error downloading or saving profile image for user {user.username}: {e}"
