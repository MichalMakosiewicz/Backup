from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab  # scheduler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backup.settings')
app = Celery('backup')
app.conf.timezone = 'UTC'
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
