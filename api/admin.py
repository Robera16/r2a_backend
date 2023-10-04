from django.contrib import admin
from .models import Post, Attachment, Likes, Comments, SavedPost
from django.contrib.auth import get_user_model

User = get_user_model()


admin.site.register(Likes)
admin.site.register(Comments)
admin.site.register(SavedPost)

class AttachmentInLine(admin.TabularInline): 
    model = Attachment 
    extra = 1

class TaggedUsersInline(admin.TabularInline):
    model = Post.tagged_users.through
    extra = 1

class SavedInLine(admin.TabularInline):
    model = SavedPost
    extra = 1

class PostAdmin(admin.ModelAdmin): 
    fieldsets = [(None, {'fields': ['description', 'clarified', 'category', 'user_id', 'constituency', 'district']}), ] 
    inlines = [TaggedUsersInline, AttachmentInLine, SavedInLine] 

admin.site.register(Post, PostAdmin) 
