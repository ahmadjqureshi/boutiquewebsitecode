"""
WSGI config for boutique project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys
sys.path = ['/root/bwebsite/boutique/'] + sys.path
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boutique.settings")
os.environ['DJANGO_SETTINGS_MODULE'] = 'boutique.settings'

#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

