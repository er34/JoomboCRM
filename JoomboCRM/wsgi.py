"""
WSGI config for JoomboCRM project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, sys
sys.path.append('C:/Bitnami/projects/JoomboCRM/')
os.environ.setdefault("PYTHON_EGG_CACHE", "C:/Bitnami/projects/JoomboCRM/egg_cache")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "JoomboCRM.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()