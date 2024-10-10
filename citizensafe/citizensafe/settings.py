# citizensafe/settings.py

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'USgrmUHfoB_rZkVN8XcdBVNYOaPeTgVK__EQbIekS5Kxgh4tCjGNl_NXsvJn8WJxpy8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

AUTH_USER_MODEL = 'citizen_interface.User'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin', # Interface d'administration de Django
    'django.contrib.auth',  # Authentification et Users
    'django.contrib.contenttypes', # Travailler avec des types de contenu génériques
    'django.contrib.sessions', # Sessions Utilisateur
    'django.contrib.messages', # Système de Messagerie pour afficher des notifications
    'django.contrib.staticfiles', # Gère les fichiers statiques (CSS, images, JS)
    'citizen_interface',
    'police_interface',
    'postman_interface',
    'rest_framework',  # Pour l'API REST
    'corsheaders',  # Pour gérer les requêtes cross-origin
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Pour CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'citizensafe.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'citizensafe.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', # Similarité avec infos User
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', # Longueur Minimale
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', # Présence dans une liste de mdp courants
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', # mdp entièrement numérique
    },
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = False  # Set to True for development, but be careful in production
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # If you're using a separate frontend (e.g., React)
]

# Email settings (for password reset, notifications, etc.)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Change this to your email provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'safecitizenship@gmail.com'
EMAIL_HOST_PASSWORD = '06groupeCS'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
    },
}

# Security settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

LOGIN_REDIRECT_URL = '/profile/'
LOGOUT_REDIRECT_URL = 'home'  # Redirection après déconnexion