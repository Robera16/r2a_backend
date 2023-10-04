from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators  import RegexValidator
from django.contrib.auth import get_user_model
User_Model = get_user_model()
from api_auth.models import Constituency, District, State
from django.db.models import Q
from django.core.exceptions import ValidationError
import os
from friendship.models import Friend, Follow

uploadTo = os.environ['ATTACHMENTS_PATH']
class Post(models.Model):
    CATEGORY_CHOICES =( 
        (1, "political"),
        (2, "medical"),
        (3, "problem"),
        (4, "feed"))
    description = models.TextField(blank=True, null=True)
    gps_data = models.CharField(max_length=255, blank=True)
    clarified = models.BooleanField(default=False)
    category = models.IntegerField(
        choices=CATEGORY_CHOICES
    )
    user_id = models.ForeignKey(User_Model, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    constituency = models.ForeignKey(Constituency, null=True, blank=True, on_delete=models.SET_NULL, related_name="posts")
    district = models.ForeignKey(District, null = True, blank=True, on_delete=models.SET_NULL, related_name="posts")
    area  = models.TextField(blank=True)
    tagged_users = models.ManyToManyField(User_Model, related_name="tagged")

    def __str__(self):
        return  self.user_id.first_name + "'s post"  if not self.description else self.description

    # -> As MEDICAL posts only have district not constituency 
    @classmethod
    def get_district_posts(cls, districtId, status):
        """
        Get all posts by districtId
        Political Posts : Get all constituencies for that district and get all posts on that constituencies  
        Medical Posts: Get all Medical Posts on that district  
        """
        constituency_list = District.objects.get(id=districtId).constituencies.all()
        if status is not None:
            return cls.objects.filter(Q(district = districtId) | Q (constituency__in = constituency_list)).filter(clarified =  status).distinct().order_by('-created_at')
        else :
            return cls.objects.filter(Q(district = districtId) | Q (constituency__in = constituency_list) ).distinct().order_by('-created_at')
    
    @classmethod
    def get_constituency_posts(cls, constituecy_id, status):
        """
            Get all posts by constituecy_id
            Poltical Posts:  All political posts with that constituency
            Medical Posts: Get the District of that constituency and get the posts on that District
        """
        district = Constituency.objects.get(id=constituecy_id).district_id;
        if status is not None:
            return cls.objects.filter( Q(constituency  = constituecy_id) | Q(district = district)).filter(clarified = status).distinct().order_by('-created_at')
        else:
            return cls.objects.filter( Q(constituency  = constituecy_id) | Q(district = district)).distinct().order_by('-created_at')
    
    @classmethod
    def get_state_posts(cls, stateId, status):
        """
            Get all Posts on state
            Medical Posts: Districts on that state get all  posts
            Political Posts: Constituencies of Districts of state
        """
        district_list = State.objects.get(id = stateId).districts.all()
        constituency_list = Constituency.objects.filter(district_id__state_id = stateId)
        if status is not None:
            return cls.objects.filter(Q(district__in = district_list) | Q (constituency__in = constituency_list)).filter(clarified = status).distinct().order_by('-created_at')
        else:
            return cls.objects.filter(Q(district__in = district_list) | Q (constituency__in = constituency_list) ).distinct().order_by('-created_at')

    @classmethod
    def get_regular_posts(cls, current_user):
        """
            For normal news-feed screen to get only category 3 and 4 related posts
        """
        following = Follow.objects.following(current_user)
        # Friend.objects.are_friends(user, current_user)
        return cls.objects.filter(Q(Q(category = 4) & Q(user_id__in = following) ) | Q(user_id = current_user) | Q(category = 3)).order_by('-created_at').distinct()

    # @TODO: Do not allow admin to set constituency id and district id to a post which are not related 
    """ Ex: He cannot keep constituency as warangal(West) and again district as vijayawada
                He can do constituency as warangal(West) and district as Warangal(Urban)
        else restrict him if constituency is selected do not let him select district

        and also make conc id or district id as mandatory for both political and medical problems respectively
     """


    """
    -------------------
    The Below Implementation makes sure that  constituency and district are not left blank if the the post is a political/medical respectively
    """
    def is_available(self):
        if(self.category == 1 and self.user_id.constituency_id == None):
            return False
        elif(self.category == 2 and self.district == None):
            return False
        else:
            return True

    def clean(self):
        print(self.attachments)
        if not self.is_available():
            raise ValidationError('Constitunecy or District  is Mandatory for a Post ')

#TODO: Investigate if attachments are getting deleted properly 
class Attachment(models.Model):
    CATEGORY_CHOICES =( 
        (1, "IMG"),
        (2, "VID"),
        (3, "OTHER"),)
    attachment = models.FileField(blank=False, upload_to=uploadTo, null=False)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='attachments')
    file_type = models.IntegerField(
        choices=CATEGORY_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def delete(self):
        self.attachment.delete(save=False)
        super().delete()

class Likes(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user_id = models.ForeignKey(User_Model, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post_id', 'user_id'], name='like object can only be one')
        ]


class Comments(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user_id = models.ForeignKey(User_Model, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.message

class SavedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved')
    user = models.ForeignKey(User_Model, on_delete=models.CASCADE, related_name="saved_posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name
    