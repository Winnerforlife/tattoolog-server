import os.path
from datetime import timedelta
import environ
from django.utils.translation import gettext_lazy as _


root = environ.Path(__file__) - 2
env = environ.Env()
environ.Env.read_env(env.str(root(), '.env'))

BASE_DIR = root()

SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.bool('DEBUG')
ALLOWED_HOSTS = [host.strip("'\"") for host in env.str('ALLOWED_HOSTS').split(' ')]

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
    'modeltranslation',
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
    'storages',
    'nested_admin',
    'admin_thumbnails',
    'ckeditor',
]

INSTALLED_APPS = THIRD_PARTY_APPS + PROJECT_APPS + DJANGO_APPS

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

SITE_ID = 1

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# STATIC_URL
public_key = env.str('DJANGO_S3_PUBLIC_KEY', None)
private_key = env.str('DJANGO_S3_PRIVATE_KEY', None)
bucket = env.str('DJANGO_S3_BUCKET_NAME', None)

if public_key and private_key and bucket:
    AWS_ACCESS_KEY_ID = public_key
    AWS_SECRET_ACCESS_KEY = private_key
    AWS_STORAGE_BUCKET_NAME = bucket
    AWS_S3_ENDPOINT_URL = 'https://fra1.digitaloceanspaces.com'
    AWS_S3_CUSTOM_DOMAIN = 'tattolog.fra1.digitaloceanspaces.com'
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_QUERYSTRING_AUTH = False
    AWS_LOCATION = ''

    STATIC_URL = 'https://%s/static/' % AWS_S3_CUSTOM_DOMAIN
    STATICFILES_STORAGE = 'config.storages.StaticStorage'

    MEDIA_URL = 'https://%s/uploads/' % AWS_S3_CUSTOM_DOMAIN
    DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'
else:
    STATIC_URL = '/config/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'config/static/')
    MEDIA_URL = '/config/uploads/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'config/uploads/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.CustomUser'
# AUTHENTICATION_BACKENDS = ['apps.accounts.backends.EmailBackend']
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

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
    "LOGIN_FIELD": "username",
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
EMAIL_HOST = 'mx.vean-tattoo.com'
EMAIL_PORT = 5587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER').strip("'\"")
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD').strip("'\"")
DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL').strip("'\"")


# CITIES_LIGHT
# CITIES_LIGHT_INCLUDE_COUNTRIES = ['PL', 'GB', 'DE', 'UA']


# LANGUAGE_CODE = "en"
LANGUAGES = (
    ("en", _("English")),
    ("uk", _("Ukrainian")),
    ("pl", _("Polish")),
    ("de", _("German")),
)
