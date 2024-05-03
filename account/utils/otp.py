import pyotp
import base64
from django.conf import settings


def get_otp_secret_key(user_id: int) -> str:
    return f"{user_id}-{settings.SECRET_KEY}"


def generate_otp(user_id: int, interval: int = 300) -> str:
    secret = base64.b32encode(get_otp_secret_key(user_id).encode())
    generated_otp = pyotp.TOTP(secret, interval=interval).now()
    return generated_otp


def verify_otp(user_id: int, otp: str, interval: int = 300) -> bool:
    secret = base64.b32encode(get_otp_secret_key(user_id).encode())
    is_verified = pyotp.TOTP(secret, interval=interval).verify(otp)
    return is_verified
