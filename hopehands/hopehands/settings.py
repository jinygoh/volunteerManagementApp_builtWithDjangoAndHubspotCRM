"""
Django settings for the HopeHands project.

This file contains the core configuration for the Django application, including
database settings, installed apps, middleware, and third-party integrations
like Django REST Framework and HubSpot.

Environment-specific variables are loaded from a .env file.
For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/
"""

import os
from pathlib import Path

# --- Core Paths and Security ---

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# The secret key is loaded from environment variables for security.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', "django-insecure-5*@=zh^(47k@y4(dgz!^o1%rce0i*l(h@thd_do83o=opug-6(")

# SECURITY WARNING: don't run with debug turned on in production!
# Debug mode is enabled based on the DJANGO_DEBUG environment variable.
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = []


# --- Application Definitions ---

INSTALLED_APPS = [
    # Standard Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',

    # Local apps
    'volunteer',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hopehands.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "hopehands.wsgi.application"


# --- Database Configuration ---
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        'ENGINE': 'mysql.connector.django',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# --- API and Third-Party Service Configuration ---

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# HubSpot API token
HUBSPOT_PRIVATE_APP_TOKEN = os.environ.get('HUBSPOT_PRIVATE_APP_TOKEN')


# --- Password Validation ---
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# --- Internationalization and Static Files ---
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = "static/"


# --- Model and Authentication Settings ---

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication URLs for the template-based views
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
