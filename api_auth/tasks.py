# from celery.task.schedules import crontab
# from celery.decorators import periodic_task
# from celery.utils.log import get_task_logger
# import requests

# logger = get_task_logger(__name__)

# # @periodic_task(run_every=(crontab(minute=1)))
# def say_hello():
#     # requests.get('http://127.0.0.1:8000/api/my_recent_posts/')
#     print("hello world")
#     logger.info("Hello There mate")

from .models import PhoneOtp, User
from celery.decorators import periodic_task
from datetime import timedelta
from celery.task.schedules import crontab
from django.utils import timezone

@periodic_task(run_every=crontab(minute="*/5"))
def reset_otps():
    reset_phone_otps()
    reset_user_otps()

def reset_phone_otps():
    time_frame = timezone.now()-timezone.timedelta(minutes=20)
    open_otps = PhoneOtp.objects.filter(attempts__gte=5, updated_at__lte=time_frame)
    open_otps.update(attempts = 0, otp= '')

def reset_user_otps():
    time_frame = timezone.now()-timezone.timedelta(minutes=20)
    users = User.objects.filter(attempts__gte=5, updated_at__lte=time_frame)
    users.update(attempts=0, otp='')