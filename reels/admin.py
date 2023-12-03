from django.contrib import admin
from .models import *

class ReelsAttachmentInLine(admin.TabularInline): 
    model = ReelsAttachment 
    extra = 1

class ReelsAdmin(admin.ModelAdmin): 
    fieldsets = [(None, {'fields': ['user_id', 'description']} )]
    inlines = [ReelsAttachmentInLine] 


admin.site.register(Reel, ReelsAdmin)
admin.site.register(ReelsAttachment)
admin.site.register(ReelLikes)
admin.site.register(ReelComments)
admin.site.register(ReelCommentLike)
admin.site.register(ReelShares)
admin.site.register(SavedReel)