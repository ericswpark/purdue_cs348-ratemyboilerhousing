import io
import os
from urllib.parse import urlparse

import environ
from google.cloud import secretmanager

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, False))
env_file = BASE_DIR / '.env'

if os.path.isfile(env_file):
    # Local env file found, use it
    env.read_env(env_file)
elif os.getenv("GOOGLE_CLOUD_PROJECT", None):
    # Pull secrets from Secret Manager
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

    env.read_env(io.StringIO(payload))
else:
    raise Exception("No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

APPENGINE_URL = env("APPENGINE_URL", default=None)
if APPENGINE_URL:
    # Ensure a scheme is present in the URL before it's processed.
    if not urlparse(APPENGINE_URL).scheme:
        APPENGINE_URL = f"https://{APPENGINE_URL}"

    ALLOWED_HOSTS = [urlparse(APPENGINE_URL).netloc]
    CSRF_TRUSTED_ORIGINS = [APPENGINE_URL]
    SECURE_SSL_REDIRECT = True
else:
    ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "core",
    "accounts",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': env.db()
}

if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES['default']['HOST'] = "127.0.0.1"
    DATABASES['default']['PORT'] = 5432

# Custom user model
AUTH_USER_MODEL = 'accounts.User'


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_ROOT = "static"
STATIC_URL = "/static/"
STATICFILES_DIRS = []

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
