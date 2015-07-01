# -*- coding: utf-8 -*-

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f^7#@b(we2ie=z-j&3fmb5!)x(^9re%uiv&%jfzmb5jr^7ism7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

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

STATIC_ROOT = 'C:/Bitnami/projects/JoomboCRM/JoomboCRM/static'

MEDIA_ROOT = 'C:/Bitnami/projects/JoomboCRM/JoomboCRM/media/'