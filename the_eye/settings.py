"""
Django settings for the_eye project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

import boto3
import botocore
import dj_database_url
import dotenv
import requests
from s3_environ import S3Environ
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env if present
dotenv.read_dotenv(os.path.join(BASE_DIR, ".env"))
ENVIRONMENT = os.environ.get("ENVIRONMENT")
LOAD_ENVS_FROM_FILE = (
    True if os.environ.get("LOAD_ENVS_FROM_FILE", False) == "True" else False
)

# If no .env / LOAD_ENVS_FROM_FILE is present,
# look for a `envs-<environment_name>.json` on a specific S3 Bucket
env_file = f"envs-{ENVIRONMENT}.json"
if not LOAD_ENVS_FROM_FILE:
    S3Environ(bucket="bucket-env", key=env_file)
    print("Loading envs from S3: {0}".format(env_file))

# Security
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = ENVIRONMENT == "development" or os.environ.get("DEBUG", False)


ALLOWED_HOSTS = [
    ".us-west-2.elb.amazonaws.com",
    ".compute-1.amazonaws.com",
    "localhost",
]

EC2_PRIVATE_IP = None
try:
    EC2_PRIVATE_IP = requests.get(
        "http://169.254.169.254/latest/meta-data/local-ipv4",
        timeout=0.01,
    ).text
except requests.exceptions.RequestException:
    pass

if EC2_PRIVATE_IP:
    ALLOWED_HOSTS.append(EC2_PRIVATE_IP)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Rest Framework
    "rest_framework",
    "rest_framework.authtoken",
    # Rest Auth
    "rest_auth",
    "rest_auth.registration",
    # Allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # Storage
    "storages",
    # CORS
    "corsheaders",
    # Django JSON Widget
    "django_json_widget",
    # Apps
    "accounts",
    "applications",
    "events",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "helpers.middleware.ApplicationKeyMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "the_eye.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "the_eye.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Authentication
AUTH_USER_MODEL = "accounts.User"
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

REST_AUTH_SERIALIZERS = {
    "LOGIN_SERIALIZER": "accounts.api.v1.serializers.LoginSerializer",
    "TOKEN_SERIALIZER": "accounts.api.v1.serializers.UserTokenSerializer",
    "USER_DETAILS_SERIALIZER": "accounts.api.v1.serializers.UserDetailsSerializer",
}

REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "accounts.api.v1.serializers.RegisterSerializer",
}

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# CORS
CORS_ALLOW_ALL_ORIGINS = True

# Storage
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_IS_GZIPPED = True
AWS_QUERYSTRING_AUTH = False
if DEBUG or ENVIRONMENT == "test":
    AWS_S3_ENDPOINT_URL = os.environ.get(
        "AWS_S3_ENDPOINT_URL", "http://localhost:4566/"
    )
    AWS_SECRET_ACCESS_KEY = "foo"
    AWS_ACCESS_KEY_ID = "foo"

    # Creates the bucket locally
    if ENVIRONMENT == "development":
        s3 = boto3.resource(
            "s3",
            endpoint_url=AWS_S3_ENDPOINT_URL,
            aws_access_key_id=AWS_SECRET_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        try:
            s3.meta.client.head_bucket(Bucket=AWS_STORAGE_BUCKET_NAME)
        except botocore.exceptions.ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "404":
                bucket = s3.Bucket(AWS_STORAGE_BUCKET_NAME)
                bucket.create(ACL="public-read")

# Redis
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

# Celery
CELERY_BROKER_URL = f"{REDIS_URL}/2"
CELERY_TASK_DEFAULT_QUEUE = os.environ.get("CELERY_DEFAULT_QUEUE", ENVIRONMENT)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "America/New_York"

if ENVIRONMENT == "test":
    CELERY_TASK_ALWAYS_EAGER = True

# Sentry & Logging
if not DEBUG and ENVIRONMENT != "test":

    def before_send(event, hint):
        # Ignore disallowed hosts
        if event.get("logger") == "django.security.DisallowedHost":
            return None
        return event

    integrations = [DjangoIntegration(), CeleryIntegration()]
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        environment=ENVIRONMENT,
        integrations=integrations,
        before_send=before_send,
    )


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "level": "WARNING",
        "handlers": ["sentry"],
    },
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "sentry": {
            "level": "ERROR",
            "class": "sentry_sdk.integrations.logging.EventHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "helpers.logging_handler.CustomStreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django.db.backends": {
            "level": "DEBUG" if DEBUG else "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "sentry.errors": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "sentry": {
            "level": "ERROR",
            "handlers": ["sentry"],
            "propagate": False,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": [
                "console",
            ],
            "propagate": False,
        },
        "amazon-logs": {
            "level": "INFO",
            "handlers": ["console"],
        },
    },
}
