"""
Django settings for monitor_serv project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

from django.contrib.messages import constants as messages
from django.urls import reverse_lazy

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
    'dashboard',
    'dashboard_detail',
    'dashboard_ivcs',
    'dashboard_users',
    # pip apps
    'bootstrap_modal_forms',
    'widget_tweaks',
    'crispy_forms',
    'crispy_bootstrap5'
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

ROOT_URLCONF = 'monitor_serv.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'dashboard/templates/dashboard',
            BASE_DIR / 'dashboard_users/templates/dashboard_users',
            BASE_DIR / 'dashboard_detail/templates/dashboard_detail',
            BASE_DIR / 'dashboard_ivcs/templates/dashboard_ivcs',
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

DATABASE_ROUTERS = (
    'logic.database_routers.IvaDashboardRouter',
    'logic.database_routers.IvcsRouter',
)

DEFAULT_IVCS_SCHEMAS = "search_path=auth,billing,instantmessaging,smpp,statistic,storage,updates,videoconference"

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.sqlite3",
        'NAME': "iva_dashboard.sqlite3",
    },
    'iva_dashboard': {
        'ENGINE': os.getenv("ENGINE", "django.db.backends.postgresql_psycopg2"),
        'NAME': os.getenv('POSTGRES_DB_NAME', "test_db"),
        'USER': os.getenv('POSTGRES_DB_USER', "test_db"),
        'PASSWORD': os.getenv('POSTGRES_DB_PASSWORD', "test_db"),
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
        'PASSWORD': os.getenv('IVCS_POSTGRES_DB_PASSWORD', "kbxa"),
        'HOST': os.getenv('IVCS_POSTGRES_DB_HOST', "localhost"),
        'PORT': os.getenv('IVCS_POSTGRES_DB_PORT', "8012")
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
            'min_length': 8
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
    # {
    #     'NAME': 'monitor_serv.password_validation.RepeatedPasswordValidator'
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "dashboard", "static"),
    os.path.join(BASE_DIR, "dashboard_detail", "static"),
    os.path.join(BASE_DIR, "dashboard_users", "static"),
    os.path.join(BASE_DIR, "dashboard_ivcs", "static"),
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom const variables
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', default="http://*localhost:8004").split(" ")

CONN_HEALTH_CHECKS = True

LOGIN_REDIRECT_URL = reverse_lazy("dashboard:dashboard")
LOGOUT_REDIRECT_URL = reverse_lazy("dashboard:index")

AUTH_USER_MODEL = "dashboard_users.CustomUser"

ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', b'Thm1rA590U9IBSMMIlKWgBSPwbP30nz4keJR6N4RXjI=')

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
 }

MAIL_TO_DEV = os.getenv("MAIL_TO_DEV", "borodinpa@css.rzd")
CALL_TO_DEV = os.getenv("CALL_TO_DEV", "77619")

SCRAPER_URL = os.getenv("SCRAPER_URL", "http://2.0.96.1:8000/api/monitor/metrics")
SCRAPE_INTERVAL = os.getenv("SCRAPE_INTERVAL", 15)

APP_VERSION = "v0.8.1"
