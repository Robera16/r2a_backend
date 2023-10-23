from django.db import models
from django.contrib.auth import get_user_model
from api.models import Post
from django.core.exceptions import ValidationError

User = get_user_model()



"""
    cause_user is who triggered that action, user is to whome it is intended to.

    Notification class is generic for all kind of notification for now (tagged in a post and some user  following you ) operations

    Tagged Post::
        if a user tags you in post "notification_type" will be 2 and we store the tagged_post with the post that he was tagged in and cause_user will be user who tagged him (post creator)
        example notification: "cause_user" tagged you in a post

    Follow post:
        if user 'A' starts to follow 'B' "notification_type" will be 1 and cause_user id will be 'A' 
        example notiication: A("cause_user") started following you
"""

TypeChoices = ((1, "Follow"), (2, "Tag"), (3, "Like"), (4, "Comment"))

class Notification(models.Model):
    notification_type = models.IntegerField(choices=TypeChoices, blank=False, null=False)
    tagged_post = models.ForeignKey(Post, related_name="post_notification", on_delete=models.CASCADE, null=True, blank=True)
    cause_user = models.ForeignKey(User, related_name="caused_notification", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE, blank=False, null=False)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


    def __str__(self):
        if self.notification_type == 1:
            return self.cause_user.first_name + " Started Following " + self.user.first_name
        elif self.notification_type == 2:
            return self.cause_user.first_name + " tagged " + self.user.first_name + " in a post " + str(self.tagged_post.id)
        elif self.notification_type == 3: 
            return self.cause_user.first_name + " liked  post " + str(self.tagged_post.id)
        else:
            return self.cause_user.first_name + " commented on a post " + str(self.tagged_post.id)


    #Validations ...
    def clean(self):
        if self.notification_type == 2 and not self.tagged_post:
            raise ValidationError("Follower Post id is mandatory for \"Tag\" notification type")




class Call(models.Model):
    caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calls_made')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calls_received')
    timestamp = models.DateTimeField(auto_now_add=True)
