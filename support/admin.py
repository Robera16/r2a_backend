from django.contrib import admin
from .models import AdminTicket, SupportTicket
admin.site.register(AdminTicket)
admin.site.register(SupportTicket)