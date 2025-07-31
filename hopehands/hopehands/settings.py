# Import necessary modules.
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# This sets the base directory for the project.
BASE_DIR = Path(__file__).resolve().parent.parent


# --- Security Settings ---

# SECURITY WARNING: keep the secret key used in production secret!
# This key is used for cryptographic signing and should be kept confidential.
SECRET_KEY = "django-insecure-5*@=zh^(47k@y4(dgz!^o1%rce0i*l(h@thd_do83o=opug-6("

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True enables detailed error pages, which can expose sensitive information.
# This should be set to False in a production environment.
DEBUG = True

# A list of strings representing the host/domain names that this Django site can serve.
ALLOWED_HOSTS = []


# --- Application Definition ---

# A list of all Django applications that are activated in this project.
INSTALLED_APPS = [
    # Standard Django applications.
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Custom application for this project.
    'volunteer',
]

# A list of middleware to be executed for each request/response.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# The root URL configuration module for the project.
ROOT_URLCONF = "hopehands.urls"

# Configuration for templates.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # Directories where the template engine should look for template source files.
        "APP_DIRS": True,  # Allows the template engine to look for templates inside application directories.
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

# The WSGI application entry point for the project.
WSGI_APPLICATION = "hopehands.wsgi.application"


# --- Database Configuration ---

# The private app token for HubSpot, retrieved from environment variables.
# This is used to authenticate with the HubSpot API.
HUBSPOT_PRIVATE_APP_TOKEN = os.environ.get('HUBSPOT_PRIVATE_APP_TOKEN')

# Database connection settings.
DATABASES = {
    "default": {
        # Using the MySQL backend.
        'ENGINE': 'django.db.backends.mysql',
        # Database credentials retrieved from environment variables.
        # This is a good practice to avoid hardcoding sensitive information.
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'localhost',  # The database host.
        'PORT': '3306',       # The database port.
    }
}


# --- Password Validation ---

# A list of validators that are used to check the strength of users' passwords.
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --- Internationalization ---

# The default language code for this installation.
LANGUAGE_CODE = "en-us"

# The time zone for this installation.
TIME_ZONE = "UTC"

# A boolean that specifies whether Django's translation system should be enabled.
USE_I18N = True

# A boolean that specifies if datetimes will be timezone-aware by default or not.
USE_TZ = True


# --- Static Files ---

# URL to use when referring to static files located in STATIC_ROOT.
STATIC_URL = "static/"

# The default primary key field type to use for models that don't have a field with primary_key=True.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
