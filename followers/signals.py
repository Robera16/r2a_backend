from friendship.signals import following_created
from django.dispatch import receiver
from notifications.models import Notification


#create a notification when user starts follwing other
#following.follower is the current user and following.followee is whome current is following  
@receiver(following_created) 
def following_relation_created(following, **kwargs):
    Notification.objects.create(notification_type=1, user=following.followee, cause_user=following.follower, seen=False)