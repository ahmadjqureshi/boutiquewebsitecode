import os
import sys
sys.path = ['/root/bwebsite/boutique'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'boutique.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

