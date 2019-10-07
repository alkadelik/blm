"""
Django settings for blm project.

Generated by 'django-admin startproject' using Django 1.11.20.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '81pyuu9tg(n@90u-08=*!bs$v*5k$04s)s@sgyb#6^@y&8$09+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '206.81.26.92', 'www.budgetlikemagic.com', 'budgetlikemagic.com']


# Application definition

INSTALLED_APPS = [
    'chris',
    'sprout',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'blm.middleware.loginRequiredMiddleware'
]

ROOT_URLCONF = 'blm.urls'

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

WSGI_APPLICATION = 'blm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'blm_db',
        'USER': 'debola',
        'PASSWORD': 'Sp#c3yutw4,!',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC' #'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

AWS_ACCESS_KEY_ID = 'SXQ5KPNY4JYHJ4V3DG5Z'
AWS_SECRET_ACCESS_KEY = 'PM+dpux9zQ0iRq9FcWRCsqwwcuYQBbW/tw7Klsj3NRE'

AWS_STORAGE_BUCKET_NAME = 'blm-space'
AWS_S3_ENDPOINT_URL = 'https://fra1.digitaloceanspaces.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
AWS_DEFAULT_ACL = 'public-read'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATIC_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, AWS_LOCATION)
STATIC_ROOT = 'static/'


LOGIN_REDIRECT_URL = '/sprout/' # goes here after logging in

LOGIN_URL = '/chris/index/'

LOGIN_EXEMPT_URLS = (
    r'^chris/logout/$',
    r'^chris/register/$',
    r'^chris/reset_password/$',
    r'^chris/password_reset/done/$',
    r'^chris/password_reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
    r'^chris/password_reset/complete/$'
)

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' #This will avoid the need for an SMTP server as e-mails will be printed to the console. For more information, please refer to: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smpt.zoho.com'
EMAIL_HOST_USER = 'debola@budgetlikemagic.com'
EMAIL_HOST_PASSWORD = 'Hd6$#jKu89'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DATE_INPUT_FORMATS = ('%d-%m-%Y','%Y-%m-%d')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
