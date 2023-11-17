from django.contrib import admin

from .models import Group, GroupMessage, OneToOneChat

admin.site.register(Group)
admin.site.register(GroupMessage)
admin.site.register(OneToOneChat)