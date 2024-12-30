"""
WSGI config for BackEnd_TravelPlanning project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BackEnd_TravelPlanning.settings")

application = get_wsgi_application()
import os
import sys


virtualenv_path = '/home/TripTide/.virtualenvs/my-virtualenv'
if virtualenv_path not in sys.path:
    sys.path.insert(0, virtualenv_path)


project_path = '/home/TripTide/BackEnd_TravelPlanning_v3'
if project_path not in sys.path:
    sys.path.append(project_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'BackEnd_TravelPlanning_v3.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()