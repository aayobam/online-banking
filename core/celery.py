import os
from celery.schedules import crontab
from celery import Celery
from __future__ import absolute_import, unicode_literals



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    'calculate_interest': {
        'task': 'calculate_interest',
        # http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html
        'schedule': crontab(0, 0, day_of_month='1'),
    }
}

@app.bind(task=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))