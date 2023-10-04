from django.db import models
from django.contrib.auth import get_user_model
import os
from django.utils import timezone
from django.db.models import Q
from friendship.models import  Follow

User = get_user_model()
uploadTo = os.environ['EVENTS_PATH']

EVENT_TYPE = (
    (1, "PUBLIC"),
    (2, "PRIVATE"),
    )
class Event(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    city = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    banner = models.FileField(upload_to=uploadTo, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    event_type = models.IntegerField(choices=EVENT_TYPE, default=1)
    start = models.DateTimeField(default=timezone.now, blank=False)
    end = models.DateTimeField(default=timezone.now, blank=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


    '''
        send private events if logged in user is following the user who created private event
        send all public events
    '''
    @classmethod
    def events_for_me(cls, user):
        following = Follow.objects.following(user)
        return cls.objects.filter(Q(Q(event_type = 2) & Q(user__in=following) | Q(event_type = 1))).distinct().order_by('-created_at')
