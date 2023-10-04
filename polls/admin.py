from django.contrib import admin
from .models import Poll, Choice, PollAnswer


class ChoiceInLine(admin.TabularInline): 
    model = Choice 
    extra = 2
    max_num = 2
class QuestionAdmin(admin.ModelAdmin): 
    fieldsets = [(None, {'fields': ['question', 'user']}), ] 
    inlines = [ChoiceInLine] 

admin.site.register(Poll, QuestionAdmin) 

admin.site.register(PollAnswer)