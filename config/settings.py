import os.path
from datetime import timedelta
import environ

root = environ.Path(__file__) - 2
env = environ.Env()
environ.Env.read_env(env.str(root(), '.env'))

BASE_DIR = root()

SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.bool('DEBUG')
# ALLOWED_HOSTS = env.str('ALLOWED_HOSTS').split(' ')
ALLOWED_HOSTS = ["*"]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

PROJECT_APPS = [
    'apps.accounts',
    'apps.portfolio',
    'apps.tools',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'drf_yasg',
    'djoser',
    'corsheaders',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular',
    'django_filters',
    'cities_light',
    'phonenumber_field',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

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

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str('PG_DATABASE'),
        "USER": env.str('PG_USER'),
        "PASSWORD": env.str('PG_PASSWORD'),
        "HOST": env.str('DB_HOST'),
        "PORT": env.str('DB_PORT'),
    }
}

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

SITE_ID = 1
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

STATIC_URL = '/config/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'config/static/')
MEDIA_URL = '/config/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'config/uploads/')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.CustomUser'
AUTHENTICATION_BACKENDS = ['apps.accounts.backends.EmailBackend']

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Project API',
    'DESCRIPTION': 'Project API description',
    'VERSION': '1.0.0',

    'SERVE_PERMISSIONS': ['rest_framework.permissions.IsAuthenticated'],
    'SERVE_AUTHENTICATION': ['rest_framework.authentication.BasicAuthentication'],

    'SWAGGER_UI_SETTINGS': {
        'DeepLinking': True,
        'DisplayOperationId': True,
    },

    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

# DJOSER CONFIG
DJOSER = {
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "SET_USERNAME_RETYPE": True,
    "SET_PASSWORD_RETYPE": True,
    # "USERNAME_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL": "reset_password_confirm/{uid}/{token}",
    "ACTIVATION_URL": "activation/{uid}/{token}/",
    "SEND_ACTIVATION_EMAIL": True,
    "SOCIAL_AUTH_TOKEN_STRATEGY": "djoser.social.token.jwt.TokenStrategy",
    "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": [
        "your redirect url",
        "your redirect url",
    ],
    "SERIALIZERS": {
        "user_create": "apps.accounts.serializers.CustomUserCreateSerializer",  # custom serializer
        "user": "djoser.serializers.UserSerializer",
        "current_user": "djoser.serializers.UserSerializer",
        "user_delete": "djoser.serializers.UserSerializer",
    },
}

# CORS HEADERS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["*"]
CORS_COOKIE_SECURE = False

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
# EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL')
EMAIL_HOST_PASSWORD = 'xllc jdtl ftgu buce'
DEFAULT_FROM_EMAIL = 'govnoreklama8@gmail.com'
EMAIL_HOST_USER = 'govnoreklama8@gmail.com'

# CITIES_LIGHT
# CITIES_LIGHT_INCLUDE_COUNTRIES = ['PL', 'GB', 'DE', 'UA']
