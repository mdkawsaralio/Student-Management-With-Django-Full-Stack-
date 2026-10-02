"""
Django settings for student project.
"""

from pathlib import Path
import os

import dj_database_url

# Load a local .env file (only used on your computer; Render uses its own env vars)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------
# Core / security
# ---------------------------------------------------------------------

SECRET_KEY = os.environ.get('SECRET_KEY', 'k+n0)cvurqb3!6nqh7e&$n22)@7b)xwz7$1g(n-ly7=-#%!ac=')

# Render sets the RENDER env var automatically, so DEBUG is False there
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = []
CSRF_TRUSTED_ORIGINS = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')

if DEBUG:
    ALLOWED_HOSTS += ['localhost', '127.0.0.1']

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# ---------------------------------------------------------------------
# Applications
# NOTE: 'cloudinary_storage' must come BEFORE 'django.contrib.staticfiles'
# ---------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'dashboard',
    'notice',
    'phonenumber_field',
    'teacher',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'student.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'student.wsgi.application'


# ---------------------------------------------------------------------
# Database (PostgreSQL on Render via DATABASE_URL, SQLite locally)
# ---------------------------------------------------------------------

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}


# ---------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ---------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------------
# Static files
# ---------------------------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []


# ---------------------------------------------------------------------
# Media files + Cloudinary
# Same code runs locally and on Render. Cloudinary is used whenever the
# 3 credentials exist (in your local .env or in Render's environment).
# ---------------------------------------------------------------------

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    'SECURE': True,
}

USE_CLOUDINARY = all([
    CLOUDINARY_STORAGE['CLOUD_NAME'],
    CLOUDINARY_STORAGE['API_KEY'],
    CLOUDINARY_STORAGE['API_SECRET'],
])

STORAGES = {
    "default": {
        "BACKEND": (
            "cloudinary_storage.storage.MediaCloudinaryStorage"
            if USE_CLOUDINARY
            else "django.core.files.storage.FileSystemStorage"
        ),
    },
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if DEBUG
            else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        ),
    },
}


# ---------------------------------------------------------------------
# Email
# ---------------------------------------------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# ---------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



