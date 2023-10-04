from celery.decorators import periodic_task
from datetime import timedelta
from celery.task.schedules import crontab
from django.utils import timezone
from .models import Story


"""
    Delete stories that are 24hrs old ..
"""
@periodic_task(run_every=crontab(minute="*/5"))
def delete_stories():
    time_frame = timezone.now()-timezone.timedelta(hours=24)
    Story.objects.filter(created_at__lte = time_frame).delete()