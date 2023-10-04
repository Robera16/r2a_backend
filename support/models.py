from django.db import models
import os
from django.contrib.auth import get_user_model
User = get_user_model()

uploadTo = os.environ['TICKET_ATTACHMENTS_PATH']

class AdminTicket(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_tickets")
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class SupportTicket(models.Model):
    CATEGORY_CHOICES =( 
        (1, "Bug Report"),
        (2, "Feature Request"),
        (3, "problem"),)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="support_tickets")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


#TODO: The below functionalities for comments and attachments are not yet implemented 
class TicketComments(models.Model):
    message = models.TextField()
    adminTicket =  models.ForeignKey(AdminTicket, on_delete=models.CASCADE, related_name="admin_comments")
    SupportTicket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name="support_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ticket_comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TicketAttachments(models.Model):
    attachment = models.FileField(blank=True, upload_to=uploadTo)
    adminTicket =  models.ForeignKey(AdminTicket, on_delete=models.CASCADE, related_name="admin_attachments")
    SupportTicket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name="support_attachments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)