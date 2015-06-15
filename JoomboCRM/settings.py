# -*- coding: utf-8 -*-

"""
Django settings for JoomboCRM project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import datetime
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), *x)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f^7#@b(we2ie=z-j&3fmb5!)x(^9re%uiv&%jfzmb5jr^7ism7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

DEFAULT_FROM_EMAIL = 'joerespublic@yandex.ru'
SERVER_EMAIL = 'joerespublic@yandex.ru'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'joerespublic@yandex.ru'
EMAIL_HOST_PASSWORD = 'By,fhvfktywbz'
FILE_CHARSET='utf-8'
DEFAULT_CHARSET='utf-8'

ALLOWED_HOSTS = []

ugettext = lambda s: s

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'clients',
    'jdirs',
    'contacts',
    'multiuser',
    'dela',
    'utils.Jdatatable',
    'projects',
    'multiuser',
    'django_bleach',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'JoomboCRM.urls'

BLEACH_ALLOWED_TAGS = ['p', 'b', 'i', 'u', 'em', 'strong', 'a']
#BLEACH_ALLOWED_ATTRIBUTES = ['href', 'title', 'style']
#BLEACH_ALLOWED_STYLES = [
#    'font-family', 'font-weight', 'text-decoration', 'font-variant']

# Strip unknown tags if True, replace with HTML escaped characters if
# False
BLEACH_STRIP_TAGS = True

# Strip comments, or leave them in.
BLEACH_STRIP_COMMENTS = False

# Use the CKEditorWidget for bleached HTML fields
#   BLEACH_DEFAULT_WIDGET = 'wysiwyg.widgets.WysiwygWidget'

WSGI_APPLICATION = 'JoomboCRM.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'joombocrmdb',
        'HOST': '',
        'PORT': '5432',
        'USER': 'bitnami',
        'PASSWORD': 'fbdfef90a2'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru'

LANGUAGES = (
   ('ru', 'Russian'),
   ('en', 'English'),
)

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# "rel" usage example
# LOCALE_PATHS=[rel('locale'),] 

STATIC_URL = '/static/'

STATIC_ROOT = 'C:/Bitnami/projects/JoomboCRM/JoomboCRM/static'

MEDIA_URL = '/media/'

MEDIA_ROOT = 'C:/Bitnami/projects/JoomboCRM/JoomboCRM/media/'


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': rel('logs\JoomboCRM'+datetime.date.today().strftime("%Y%m%d")+'.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'clients': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'contacts': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'dela': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'projects': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'utils.Jdatatable': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}