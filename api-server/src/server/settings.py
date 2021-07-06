"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import pathlib
import json
import secrets
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import django.db.models

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
SECRET_FILE = pathlib.Path(BASE_DIR).joinpath('secrets.txt')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

PRODUCTION = os.getenv('PRODUCTION')

# SECURITY WARNING: keep the secret key used in production secret!

if PRODUCTION is None:
    SECRET_KEY = '%yg))7dqy#6c=l2cu+#%28tfg4p1n29c7xwc5%%tk8*hbv2o2e'

elif PRODUCTION is not None and SECRET_FILE.is_file():
    SECRET_KEY = SECRET_FILE.read_text()

else:
    SECRET_KEY = secrets.token_urlsafe(64)
    SECRET_FILE.write_text(SECRET_KEY)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = PRODUCTION is None

ALLOWED_HOSTS = [
    'localhost',
    '.jtf191.com',
    'api-server'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'token_auth',
    'channels',
    'roster',
    'gci',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'server.urls'

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

WSGI_APPLICATION = 'server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

if PRODUCTION is None:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'database',
            'USER': 'root',
            'PASSWORD': 'my-secret-pw',
            'HOST': 'db',
            'PORT': '5432'
        }
    }

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [('redis', 6379)],
                "capacity": 5000,
                "expiry": 5
            },
        },
    }

else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'database',
            'USER': 'postgres',
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'HOST': 'db-postgresql.default.svc.cluster.local',
            'PORT': '5432'
        }
    }

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [('redis', 6379)],
                "capacity": 5000,
                "expiry": 5
            },
        },
    }


DEFAULT_AUTO_FIELD = django.db.models.BigAutoField

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


ASGI_APPLICATION = 'server.routing.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7.5),
}

# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:8080',
# ]

CORS_ORIGIN_ALLOW_ALL = True

EMAIL_SECRET_PATH = pathlib.Path(BASE_DIR).joinpath('cred.json')

if EMAIL_SECRET_PATH.is_file():

    EMAIL_SECRET = json.loads(EMAIL_SECRET_PATH.read_text())

else:

    EMAIL_SECRET = {}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = SERVER_EMAIL = EMAIL_SECRET.get('host', 'test@test.com')
EMAIL_HOST_PASSWORD = EMAIL_SECRET.get('password')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
