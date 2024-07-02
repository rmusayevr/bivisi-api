"""
Django settings for bivisi project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path
from import_export.formats.base_formats import CSV, XLSX
from bivisi.jazzmin import JAZZMIN_SETTINGS, JAZZMIN_UI_TWEAKS

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-m$pctt(_0zrns4$^cgmdgufmff(#l8)i6s0!f+d86-hy#e#iz9'

SECRET_KEY = os.environ.get(
    'SECRET_KEY', 'django-insecure-m$pctt(_0zrns4$^cgmdgufmff(#l8)i6s0!f+d86-hy#e#iz9')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", default=1))
PROD = int(os.environ.get("PROD", default=0))


ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

# Application definition
INSTALLED_APPS = [
    'daphne',
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'mptt',
    'rest_framework',
    'django_filters',
    'parler',
    'corsheaders',
    'rest_framework_simplejwt',
    'rest_framework_swagger',
    'drf_yasg',
    'django_rest_passwordreset',
    "phonenumber_field",
    'import_export',
    'storages',

    'account.apps.AccountConfig',
    'core.apps.CoreConfig',
    'product.apps.ProductConfig',
    'order.apps.OrderConfig',
    'history.apps.HistoryConfig',
    'notification.apps.NotificationConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bivisi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bivisi.wsgi.application'
ASGI_APPLICATION = 'bivisi.asgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',

#     }
# }

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('POSTGRES_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('POSTGRES_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('POSTGRES_USER', ''),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': os.environ.get('POSTGRES_HOST', ''),
        'PORT': os.environ.get('POSTGRES_PORT', '')
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'bivisi',
#         'USER': 'root',
#         'PASSWORD': 'root123',
#         'HOST': 'db',
#         'PORT': 5432
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
    MEDIA_ROOT = BASE_DIR / "media"
    MEDIA_URL = '/media/'
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    AWS_ACCESS_KEY_ID = 'AKIATCKAOUIJN6CUS7GS'
    AWS_SECRET_ACCESS_KEY = '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'
    AWS_STORAGE_BUCKET_NAME = 'bivisi-media'
    AWS_S3_SIGNATURE_NAME = 's3v4',
    AWS_S3_REGION_NAME = 'eu-central-1'
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_S3_VERITY = True
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    )
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADERS_TYPES": ("JWT",),
    "USER_ID_FIELDS": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}

CORS_ALLOW_ALL_ORIGINS = True

AUTH_USER_MODEL = 'account.User'
AUTHENTICATION_BACKENDS = ['account.backends.EmailBackend']

EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 587)
EMAIL_USE_TLS = int(os.environ.get("EMAIL_USE_TLS", default=1))
EMAIL_USE_SSL = int(os.environ.get("EMAIL_USE_SSL", default=0))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "rasmusayevhad@gmail.com")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "djupquhlwhdykhmi")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


IMPORT_EXPORT_FORMATS = [CSV, XLSX]

JAZZMIN_SETTINGS = JAZZMIN_SETTINGS
JAZZMIN_UI_TWEAKS = JAZZMIN_UI_TWEAKS

# Maximum size of file uploads in bytes (1 GB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 1024  # 1 GB
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 1024  # 1 GB

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}
