"""
Django settings for monitor_serv project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

from django.contrib.messages import constants as messages
from django.urls import reverse_lazy

import common.dbrouters
from common.dbrouters import IvaDashboardRouter, IvcsRouter

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "change_me")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv("DEBUG", True))

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", default=["*"])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # custom apps
    'api',
    'dashboard',
    'dashboard_ivcs',
    'dashboard_users',
    # pip apps
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'monitor_serv.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ]
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

WSGI_APPLICATION = 'monitor_serv.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DEFAULT_IVCS_SCHEMAS = "search_path=auth,billing,instantmessaging,smpp,statistic,storage,updates,videoconference"

DATABASE_ROUTERS = (
    # 'common.dbrouters.IvaDashboardRouter',
    'common.dbrouters.IvcsRouter',
)

DATABASES = {
    'default': {
        'ENGINE': os.getenv("ENGINE", "django.db.backends.postgresql_psycopg2"),
        'NAME': os.getenv('POSTGRES_DB_NAME', "admin_test"),
        'USER': os.getenv('POSTGRES_DB_USER', "admin_test"),
        'PASSWORD': os.getenv('POSTGRES_DB_PASSWORD', "iva_dashboard_test"),
        'HOST': os.getenv('POSTGRES_DB_HOST', "localhost"),
        'PORT': os.getenv('POSTGRES_DB_PORT', "8002"),
    },
    'ivcs': {
        'ENGINE': os.getenv("ENGINE", "django.db.backends.postgresql_psycopg2"),
        'OPTIONS': {
            'options': f'-c {os.getenv("IVCS_SCHEMAS", DEFAULT_IVCS_SCHEMAS)}'
        },
        'NAME': os.getenv('IVCS_POSTGRES_DB_NAME', "ivcs"),
        'USER': os.getenv('IVCS_POSTGRES_DB_USER', "ivcs"),
        'PASSWORD': os.getenv('IVCS_POSTGRES_DB_PASSWORD', "ivcs"),
        'HOST': os.getenv('IVCS_POSTGRES_DB_HOST', "localhost"),
        'PORT': os.getenv('IVCS_POSTGRES_DB_PORT', "8002")
    }

}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'dashboard_users.password_validation.SymbolsPasswordValidator'
    },
    {
        'NAME': 'dashboard_users.password_validation.UppercasePasswordValidator'
    },
    {
        'NAME': 'dashboard_users.password_validation.NumberPasswordValidator'
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/backend/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom const variables
CSRF_TRUSTED_ORIGINS = os.getenv(
    'CSRF_TRUSTED_ORIGINS',
    default="http://*localhost:8004 http://*localhost:3000 http://*localhost:3001 http://*127.0.0.1:3000 "
            "http://*127.0.0.1:3001"
).split()

CONN_HEALTH_CHECKS = True

AUTH_USER_MODEL = "dashboard_users.CustomUser"

ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', b'Thm1rA590U9IBSMMIlKWgBSPwbP30nz4keJR6N4RXjI=')

DATETIME_FORMAT = "%d/%m/%y %H:%M:%S"

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication'
    ]
}

if not DEBUG:
    REST_FRAMEWORK.update({
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        )
    })

    CORS_ALLOWED_ORIGIN_REGEXES = (
        "http:\/\/(localhost|(1|2|10|127).0.(0|96).(1|11|49|50)):(80|[38]00[0-9])",
    )

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)
CORS_ALLOW_HEADERS = (
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)

CORS_ALLOW_CREDENTIALS = True

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#     'ROTATE_REFRESH_TOKENS': True,
#     'BLACKLIST_AFTER_ROTATION': True,
# }

APP_VERSION = "v0.8.64"
