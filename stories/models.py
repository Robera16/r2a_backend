from django.db import models
from django.contrib.auth import get_user_model
import os
from django.core.exceptions import ValidationError
from friendship.models import Follow
from django.db.models import Q


User = get_user_model()

uploadTo = os.environ['STORIES_PATH']


MEDIA_TYPE = (
    (1, "IMG"),
    (2, "VID"),
    (3, 'TEXT'),
    (4, "OTHER"),
    )
class Story(models.Model):
    file = models.FileField(upload_to=uploadTo, blank=True)
    text = models.TextField(blank=True)
    media_type = models.IntegerField(choices=MEDIA_TYPE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stories")
    seen_by = models.ManyToManyField(User, related_name='seen_stories', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.first_name

    def clean(self):
        if(self.media_type ==  1 or self.media_type == 2):
            if(self.file == None or self.file == ''):
                raise ValidationError('Media for this story type is mandatory')
        elif(self.media_type == 3):
            if (self.text == None or self.text == ''):
                raise ValidationError('Text for this story type is mandatory')
        elif(self.media_type == 4):
            raise ValidationError("UnSupported Media Type")
    
    #remove repeated elements in a array preserving sequence.
    def remove_duplicate(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]
    
    @classmethod
    def get_user_stories(cls, user):
        """
            -> get all stories for users that current user is following 
            -> get their stories and sort them by stort created_at and exclude current user from it
            -> add current user to duplicates removed list and check all the users with stories and append it to an array and retunr it 
        """
        followers = Follow.objects.following(user)
        user_ids = [follower.id for follower in followers]
        qs = User.objects.filter(Q(pk__in = user_ids) & ~Q(id = user.id)).order_by("-stories__created_at")
        users_arr = cls.remove_duplicate(list(qs))
        # send current users stories 
        # users_arr.insert(0, user)
        list_with_stories = []
        for follow in users_arr:
            stories = follow.stories.all()
            if stories.exists():
                list_with_stories.append(follow)
        return list_with_stories