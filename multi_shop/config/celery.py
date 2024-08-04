from celery import Celery
from kombu import Exchange, Queue
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.task_queues = [
    Queue('tasks', Exchange('tasks'), routing_key='tasks',
          queue_arguments={'x-max-priority': 10}),
    Queue('dead_letter', routing_key='dead_letter'),
]

app.conf.task_default_priority = 5
app.conf.worker_concurrency = 1
worker_prefetch_multiplier = 1
app.conf.task_acks_late = True

app.autodiscover_tasks()
