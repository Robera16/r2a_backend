from django.db import models
from django.contrib.auth import get_user_model
User_Model = get_user_model()

# Create your models here.
class Poll(models.Model):
    question = models.CharField(max_length=200)
    user = models.ForeignKey(User_Model, on_delete=models.CASCADE, related_name="poll_questions")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


    def __str__(self):
        return self.question

class Choice(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="choices")
    choice = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.choice

class PollAnswer(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="question_answers")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="choice_answers")
    user = models.ForeignKey(User_Model, on_delete=models.CASCADE, related_name="poll_answers")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user.first_name

class PollComment(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User_Model, on_delete=models.CASCADE, related_name="poll_comments")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.text