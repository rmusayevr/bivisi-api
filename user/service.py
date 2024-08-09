from random import SystemRandom
from typing import Any
from urllib.parse import urlencode

import jwt
import requests
from attrs import define
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from oauthlib.common import UNICODE_ASCII_CHARACTER_SET

from user.exception import ApplicationError


@define
class GoogleRawLoginCredentials:
    client_id: str
    client_secret: str
    project_id: str


@define
class GoogleAccessTokens:
    id_token: str
    access_token: str

    def decode_id_token(self) -> dict[str, str]:
        id_token = self.id_token
        decoded_token = jwt.decode(jwt=id_token, options={
                                   "verify_signature": False})
        return decoded_token


class GoogleRawLoginFlowService:
    # API_URI = reverse_lazy("callback-raw")

    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
    GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    SCOPES = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid",
    ]

    def __init__(self):
        self._credentials = google_raw_login_get_credentials()

    @staticmethod
    def _generate_state_session_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
        # This is how it's implemented in the official SDK
        rand = SystemRandom()
        state = "".join(rand.choice(chars) for _ in range(length))
        return state

    def _get_redirect_uri(self):
        return f"{settings.BASE_FRONTEND_URL}"

    def get_authorization_url(self):
        redirect_uri = self._get_redirect_uri()

        state = self._generate_state_session_token()

        params = {
            "response_type": "code",
            "client_id": self._credentials.client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(self.SCOPES),
            "state": state,
            "access_type": "offline",
            "include_granted_scopes": "true",
            "prompt": "select_account",
        }

        query_params = urlencode(params)
        authorization_url = f"{self.GOOGLE_AUTH_URL}?{query_params}"

        return authorization_url, state

    def get_tokens(self, *, code: str) -> GoogleAccessTokens:
        redirect_uri = self._get_redirect_uri()

        # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#obtainingaccesstokens
        data = {
            "code": code,
            "client_id": self._credentials.client_id,
            "client_secret": self._credentials.client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        response = requests.post(
            self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

        if not response.ok:
            raise ApplicationError(
                "Failed to obtain access token from Google.")

        tokens = response.json()
        google_tokens = GoogleAccessTokens(
            id_token=tokens["id_token"], access_token=tokens["access_token"])

        return google_tokens

    def get_user_info(self, *, google_tokens: GoogleAccessTokens) -> dict[str, Any]:
        access_token = google_tokens.access_token
        # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#callinganapi
        response = requests.get(self.GOOGLE_USER_INFO_URL, params={
                                "access_token": access_token})

        if not response.ok:
            raise ApplicationError("Failed to obtain user info from Google.")

        return response.json()


def google_raw_login_get_credentials() -> GoogleRawLoginCredentials:
    client_id = settings.GOOGLE_OAUTH2_CLIENT_ID
    client_secret = settings.GOOGLE_OAUTH2_CLIENT_SECRET
    project_id = settings.GOOGLE_OAUTH2_PROJECT_ID

    if not client_id:
        raise ImproperlyConfigured("GOOGLE_OAUTH2_CLIENT_ID missing in env.")

    if not client_secret:
        raise ImproperlyConfigured(
            "GOOGLE_OAUTH2_CLIENT_SECRET missing in env.")

    if not project_id:
        raise ImproperlyConfigured("GOOGLE_OAUTH2_PROJECT_ID missing in env.")

    credentials = GoogleRawLoginCredentials(
        client_id=client_id, client_secret=client_secret, project_id=project_id)

    return credentials


class FacebookLoginFlowService:
    FACEBOOK_AUTH_URL = "https://www.facebook.com/v12.0/dialog/oauth"
    FACEBOOK_ACCESS_TOKEN_URL = "https://graph.facebook.com/v12.0/oauth/access_token"
    FACEBOOK_USER_INFO_URL = "https://graph.facebook.com/me"

    SCOPES = ["email", "public_profile"]

    def __init__(self):
        self._app_id = settings.FACEBOOK_APP_ID
        self._app_secret = settings.FACEBOOK_APP_SECRET

    def _generate_state_session_token(self, length=30):
        import random
        import string
        rand = random.SystemRandom()
        state = ''.join(rand.choices(string.ascii_letters + string.digits, k=length))
        return state

    def _get_redirect_uri(self):
        return f"{settings.BASE_FRONTEND_URL}"

    def get_authorization_url(self):
        redirect_uri = self._get_redirect_uri()
        state = self._generate_state_session_token()

        params = {
            "client_id": self._app_id,
            "redirect_uri": redirect_uri,
            "state": state,
            "scope": ",".join(self.SCOPES),
        }

        authorization_url = f"{self.FACEBOOK_AUTH_URL}?{urlencode(params)}"
        return authorization_url, state

    def get_tokens(self, code):
        redirect_uri = self._get_redirect_uri()

        data = {
            "client_id": self._app_id,
            "redirect_uri": redirect_uri,
            "client_secret": self._app_secret,
            "code": code,
        }

        response = requests.get(self.FACEBOOK_ACCESS_TOKEN_URL, params=data)
        response.raise_for_status()
        tokens = response.json()
        return tokens

    def get_user_info(self, access_token):
        params = {
            "fields": "id,name,email,picture",
            "access_token": access_token,
        }

        response = requests.get(self.FACEBOOK_USER_INFO_URL, params=params)
        response.raise_for_status()
        return response.json()
