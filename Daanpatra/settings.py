"""
Django settings for Daanpatra project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nceu=p5obwf32wbb!f$-5ije&bf^p5!w+vvgj5zq!e*t$=ccxf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'DaanpatraApp',
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',
    'instagram_profile',
    'corsheaders'
]

REST_FRAMEWORK = { 
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication', 
        'rest_framework_social_oauth2.authentication.SocialAuthentication'
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ] 
} 

INSTAGRAM_PROFILE = {
    # You will get these from your registered instagram app
    'app_id': '3622581841130142',
    'secret': 'f778c490c996896089e88400848385e3',
    'redirect_url': 'http://127.0.0.1:8000/',        
}


AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)


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

ROOT_URLCONF = 'Daanpatra.urls'

CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.example\.com$",
]
CORS_ALLOW_ALL_ORIGINS = True

OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 36000,
}


FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": "AAAANSv3sDw:APA91bEgoMXu74uPlgqSDlPMLhew0KceqnnLwqfPglk2uZ_PNd01EDbZ3TLx8cGP11lmbgqV3Vii3DIlH_fhTMhzcUdMUzOQjWcYowtOhlLVLPS3EkVHnmmXvhFAlJ8AOjNIfCIjZd"
}


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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect'
            ],
        },
    },
]

WSGI_APPLICATION = 'Daanpatra.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'DaanpatraApp.User'

CLIENT_ID = '04DpVJlIWfxGAMsNwMqJzkBpG654VpzCbnEz1meb'
CLIENT_SECRET = 'XniDVIbxp8Ij1bI9tWiC9TE1AsdU3E40vbPLDP1xDfbXup5cE2lLPKJalbXs50yKMuPbqZMUubAAqyPXyVhxPyb44rFSASvgpy0p8uBC8OTzyM9o0fvdpt50uSWoQlVe'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1075097280260-go5b9dkfprc6pc13ael7kdjs11i6ut2i.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '3uZF2mn0LqHlwW3c2RI09Vq9'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STRIPE_API_KEY = 'sk_test_51I99M9LRgnbH7KkbI3cQmnKYU22ReiPYOfWl7mpePqNcm00it3kAnfVfsgEJKw09Fn4THcuuzUWVPaMHRMarYE2Z008tAkQILh'

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]