import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECRET_KEY = 'ta+!s9o!33glckm!o9n1&z#o+gxf%d#q@@9t+%cvz5_6c@qcha'
# SECRET_KEY = os.getenv("SECRET_KEY",)
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'colorfield',
    'django_filters',
    'app.apps.AppConfig',

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

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'foodgram.wsgi:application'


# DATABASES = {
    # 'default': {
        # 'ENGINE': os.getenv(
           #  'DB_ENGINE', default='django.db.backends.postgresql'),
        # 'NAME': os.getenv('DB_NAME', default='postgres'),
        # 'USER': os.getenv('POSTGRES_USER', default='postgres'),
        # 'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
        # 'HOST': os.getenv('DB_HOST', default='db'),
        # 'PORT': os.getenv('DB_PORT', default=5432)
    # }
# }

DATABASES = { 
    'default': { 
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'), 
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


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PAGINATION_CLASS': 'app.pagination.CustomPagination',
    'PAGE_SIZE': 10,

}


DJOSER = {
    'LOGIN_FIELD': 'email',
    'HIDE_USERS': False,
    'SERIALIZERS': {
        'user_create': 'app.serializers.UserRegistrationSerializer',
        'user': 'app.serializers.CustomUserSerializer',
        'current_user': 'app.serializers.CustomUserSerializer',

    },
    'PERMISSIONS': {
        'user': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
        'user_list': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
    }
}
