from .models import Post, Attachment, Comments, Likes
from django.db.models.signals import pre_save, post_delete, m2m_changed, post_save
from django.dispatch import receiver
import os
from notifications.models import Notification
from utils.notifications import send_push_notification

#Add that posts users constitency to post if it is a political post
@receiver(pre_save, sender=Post)
def add_constituency_to_post(sender, instance, **kwargs):
    if not instance.user_id.is_admin:
        if instance.category == 1:
            constituency = instance.user_id.constituency_id
            instance.constituency = constituency

def post_tags_changed(sender, instance, action, **kwargs):
    if action == 'post_add':
        creator = instance.user_id
        tagged_users = instance.tagged_users.all()
        try: 
            for user in tagged_users:
                notification, created = Notification.objects.get_or_create(notification_type=2, tagged_post=instance, user=user, cause_user=creator, seen=False)
        except Exception as e:
            print(e)


'''
    only create notification for like or comment if user did not 
    like or comment his post.
'''
def create_comment_notifications(sender, instance, created, **kwargs):
    if  not (instance.post_id.user_id ==  instance.user_id):
        Notification.objects.create(notification_type=4, user=instance.post_id.user_id, tagged_post=instance.post_id, cause_user=instance.user_id)
        notification_dict = {
                        "collapse_key": "r2a",
                        "to": "token",
                        "notification": {
                            "title": "Commented on a post",
                            "body": "{name} commented on your post.".format(name=instance.user_id.first_name)
                            },
                        "data": {
                            "click_action": "FLUTTER_NOTIFICATION_CLICK",
                            "comment" : {
                            "id" : instance.post_id.id
                            }
                        },
                        "priority": 10
                    }
        send_push_notification(instance.user_id, instance.post_id.user_id, notification_dict)

def create_like_notifications(sender, instance, created, **kwargs):
    if not (instance.post_id.user_id == instance.user_id):
        Notification.objects.create(notification_type=3, user=instance.post_id.user_id, tagged_post=instance.post_id, cause_user=instance.user_id)
        notification_dict = {
                        "collapse_key": "r2a",
                        "to": "token",
                        "notification": {
                            "title": "Liked your post",
                            "body": "{name} liked your post.".format(name=instance.user_id.first_name)
                            },
                        "data": {
                            "click_action": "FLUTTER_NOTIFICATION_CLICK",
                            "like" : {
                            "id" : instance.post_id.id
                            }
                        },
                        "priority": 10
                    }
        send_push_notification(instance.user_id, instance.post_id.user_id, notification_dict)

pre_save.connect(add_constituency_to_post, sender=Post)
m2m_changed.connect(post_tags_changed, sender=Post.tagged_users.through)
post_save.connect(create_comment_notifications, sender=Comments)
post_save.connect(create_like_notifications, sender=Likes)