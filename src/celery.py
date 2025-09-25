# src/celery.py
import os
from celery import Celery

# set the default Django settings module for celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

app = Celery("src")

# load settings from Django's settings.py (CELERY_ prefix)
app.config_from_object("django.conf:settings", namespace="CELERY")

# auto-discover tasks from all installed apps
app.autodiscover_tasks()
