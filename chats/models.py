from django.db import models
from api_auth.models import User
import os
# Create your models here.


group_icons_path=os.environ['GROUP_IMAGES_PATH']
#TODO: remove when  creator leaves the group(else just remove from recepients)
#TODO: investigate if user is deleted what to do CASCASE is set now may be change to set null or else Anaonymous user or some thing like that 

class Group(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User, related_name='group_creator', on_delete=models.CASCADE)
    recepients = models.ManyToManyField(User, related_name='group_users')
    multitenant = models.BooleanField(default=True)
    avatar = models.ImageField(blank=True, upload_to=group_icons_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Group, self).save(*args, **kwargs)
        self.recepients.add(self.creator)

    def __str__(self):
        return self.name

    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return ""


class GroupMessage(models.Model):
    message = models.TextField()
    creator = models.ForeignKey(User, related_name="message_creator", on_delete=models.CASCADE)
    read_by = models.ManyToManyField(User, related_name='message_ready_by')
    room = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}'s Message by {}".format(self.room.name, self.creator.first_name) 



class OneToOneChat(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sender.username} to {self.recipient.username} ({self.created_at})'