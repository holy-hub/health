from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health.settings') # Set the default Django settings module for the 'celery' program.

app = Celery('health')
app.config_from_object('django.conf:settings', namespace='CELERY') # Using a string here means the worker doesn't have to serialize the configuration object to child processes.
app.autodiscover_tasks() # Load task modules from all registered Django app configs.

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

"""
celery -A health worker --loglevel=info # Démarrer Celery

# Démarrer Celery Beat
celery -A health beat --loglevel=info

celery -A health worker --beat --loglevel=info
"""