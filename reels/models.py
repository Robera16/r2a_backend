from django.db import models
from django.contrib.auth import get_user_model
import os
User_Model = get_user_model()
uploadTo = os.environ['REELS_PATH']

class Reel(models.Model):
    user_id = models.ForeignKey(User_Model, on_delete=models.CASCADE, default=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.description


class ReelsAttachment(models.Model):
    CATEGORY_CHOICES =( 
        (1, "IMG"),
        (2, "VID"),
        (3, "OTHER"),)
    attachment = models.FileField(blank=False, upload_to=uploadTo, null=False)
    reel_id = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name='attachments')
    file_type = models.IntegerField(
        choices=CATEGORY_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def delete(self):
        self.attachment.delete(save=False)
        super().delete()



class ReelLikes(models.Model):
    reel_id = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name='likes')
    user_id = models.ForeignKey(User_Model, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f"Reel: {self.reel_id}, User: {self.user_id}"


class ReelComments(models.Model):
    reel_id = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name='comments')
    user_id = models.ForeignKey(User_Model, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.message

class ReelCommentLike(models.Model):
    comment_id = models.ForeignKey(ReelComments, on_delete=models.CASCADE, related_name='comment_like')
    user_id = models.ForeignKey(User_Model, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Comment '{self.comment_id}' Liked by: {self.user_id}"

class ReelShares(models.Model):
    reel_id = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name='shares')
    user_id = models.ForeignKey(User_Model, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Reel {self.reel_id} shared by {self.user_id}"


class SavedReel(models.Model):
    reel_id = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name='saved')
    user_id = models.ForeignKey(User_Model, on_delete=models.CASCADE, related_name="saved_reels")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return f"Reel: {self.reel_id}, User: {self.user_id}"
