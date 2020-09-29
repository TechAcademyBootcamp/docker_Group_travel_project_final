"""
Django settings for trip_project project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
#username:serveradmin
#password:serveradmin
#fullname:amilalizada
#docker exec -t 6051dff42709 pg_dumpall -c -U trip_db_name > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql


from pathlib import Path
import os
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xy$ncdo1+i-bwuej@c!7(wk37*h_4h#-%g8i3wv$e30m75+x6s'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = not os.environ.get('DEBUG', False)
PROD = not DEBUG

ALLOWED_HOSTS = ['*']


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'tech.academy.user2@gmail.com'
EMAIL_HOST_PASSWORD = 'fsqcyadagqipthcz'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# Application definition

INSTALLED_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.sites',
    'stripe',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',  
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'ckeditor',
    'ckeditor_uploader',
    'corsheaders',
    'Account',
    'Hotels',
    'Main',
    'Restaurants',
    
    'Tours',
    'Places',
    'django_celery_beat',
]

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]


SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '940006685302-denq7k02lpicujnguj6oh6bnrv1pp15a.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'SCT2MsHw9I28MWvLAbXDQGLx'

SOCIAL_AUTH_FACEBOOK_KEY = "616088999077800"        
SOCIAL_AUTH_FACEBOOK_SECRET = "56e7d70977075eb67c2b516571fb6c07"

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email', # needed starting from protocol v2.4
}


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

ROOT_URLCONF = 'trip_project.urls'

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

WSGI_APPLICATION = 'trip_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if PROD:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('POSTGRES_DB'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': os.environ.get('POSTGRES_HOST'),
            'PORT': os.environ.get('POSTGRES_PORT')
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'trip_db_name',
            'USER': 'trip_user_name',
            'PASSWORD': '123',
            'HOST': 'localhost',
            'PORT': '5432'
        }
    }



AUTH_USER_MODEL = 'Account.User'


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Baku'

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'az'

TIME_ZONE = 'Asia/Baku'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
import os

STATIC_URL = '/static/'

if PROD:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
else:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static')
    ]

LOGIN_URL = reverse_lazy('accounts:login')
LOGIN_REDIRECT_URL = reverse_lazy('main:home')
LOGOUT_REDIRECT_URL = reverse_lazy('account:login')


GOUT_REDIRECT_URL = 'home'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'tech.academy.user2@gmail.com'
EMAIL_HOST_PASSWORD = 'fsqcyadagqipthcz'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR,'media')

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_FILENAME_GENERATOR = 'Main.utils.get_filename'
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_RESTRICT_BY_DATE = True

CKEDITOR_CONFIGS = {
    "default":{
        'height':'100%',
        'width':'100%',
    }
}

CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://sub.example.com",
    "http://localhost:8080",
    "http://127.0.0.1:9000"
]

CORS_ALLOW_ALL_ORIGINS= True

STRIPE_PUBLISHABLE_KEY = 'pk_test_51HRkMbF1lulHJpCgiLbhB9twJlb0eKfKpoYysi83t21e0AoggRB1Uk4YWRCnpz9W7gnpIYbx6rn77wHVKVl3YJcv00ilvU0tE0'
STRIPE_SECRET_KEY = 'sk_test_51HRkMbF1lulHJpCgsfHy0nItoH7jlFlbyrSVP2IvlWMWo8V8pb1TcRHKHMqSbBCLIi1Vec5T7AVoMlLENUIXHJxw00CIwUA54d'