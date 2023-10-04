from django.db import models
import time
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
from django.core.validators  import RegexValidator
from django.core.exceptions import ValidationError
from friendship.models import Friend, Follow
import os 
import datetime
date_time = datetime.datetime.now()

ProfileAttachmentsUrl = os.environ['PROFILE_PICTURES_PATH']

bucker_path = os.environ['AWS_STORAGE_BUCKET_NAME']
s3Path = "https://{path}.s3.amazonaws.com/".format(path = bucker_path) + 'user_avatars/hide.gif'
class Country(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=200)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')
    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=200)
    state_id = models.ForeignKey(State, on_delete=models.CASCADE, related_name='districts')
    def __str__(self):
        return self.name

class Constituency(models.Model):
    name = models.CharField(max_length=200)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name='constituencies')
    def __str__(self):
        return self.name

class User (AbstractBaseUser):
    first_name = models.CharField(max_length=30, blank=False)
    active = models.BooleanField(default=True)
    username = models.CharField(max_length=20,blank=False, null=False, unique=True, default='USERNAME')
    phone_number = models.CharField(validators=[RegexValidator(
                                                regex=r'^\+?1?\d{10,15}$',
                                                message = 'phone_number must be 10-15  digits long',
                                                code = 'invalid phone_number'
                                                )], unique=True, max_length=15, blank=False)
    otp = models.CharField(max_length=6, default='', blank=True, null=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, null=True,  blank=True)
    can_create = models.BooleanField(default=True)
    foreign_user = models.BooleanField(default=False)
    ROLE_CHOICES =( 
    (1, "political_rep"),
    (2, "medical_rep"),
    (3, "user")
    )

    role = models.IntegerField(choices=ROLE_CHOICES, default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    anonymous = models.BooleanField(default=False)
    country = models.ForeignKey(Country, null = True, blank=True, on_delete=models.SET_NULL, related_name="users")
    attempts = models.IntegerField(default=0)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [ 'first_name', 'phone_number']


    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.first_name 

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_active(self):
        return self.active

    @property
    def is_role(self):
        return self.role

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_anonymous(self):
        return self.anonymous

    def is_available(self):
        if (self.country != None):
            if self.country.name.lower() != "india":
                self.foreign_user = True
        
       
        if(self.admin != True and self.country == None):
            return False, "Country is Mandatory for non-admin users"
        else:
            return True, None

    def clean(self):
        validatity, message = self.is_available()
        # remove spaces in username.
        self.username = self.username.replace(' ', '')

        if not validatity:
            raise ValidationError(message)


class PhoneOtp(models.Model):
    phone_number = models.CharField(validators=[RegexValidator(
                                                regex=r'^\+?1?\d{10,15}$',
                                                message = 'phone_number must be 10-15  digits long',
                                                code = 'invalid phone_number'
                                                )], unique=True, max_length=15)
    country = models.ForeignKey(Country,  on_delete=models.SET_NULL, null=True)
    otp = models.CharField(max_length=6)
    attempts = models.IntegerField(default=0)
    validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return str(self.phone_number) + '\'s OTP is ' + str(self.otp)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, upload_to= ProfileAttachmentsUrl )
    bio = models.TextField(null=True, blank=True)
    # avatar = models.CharField(blank=True, max_length=200)
    location = models.CharField(blank=True, max_length=200)
    banner = models.CharField(blank=True, max_length=200)
    anonymous_avatar =  models.ImageField(blank=True, upload_to= ProfileAttachmentsUrl, default = 'user_avatars/hide.gif' ) 
    
    SEX_CHOICES =( 
    (1, "Male"),
    (2, "Female"),
    (3, "private"))

    sex = models.SmallIntegerField(choices=SEX_CHOICES, default=3)
    dob = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return '{name}\'s profile'.format(name=self.user.first_name)

    def mainAvatar(self):
        if self.avatar and hasattr(self.avatar, 'url'):
                return self.avatar.url
        else:
            return s3Path
    def anonymousAvatar(self):
        if self.anonymous_avatar and hasattr(self.anonymous_avatar, 'url'):
            return self.anonymous_avatar.url
        else:
            s3Path
    #@FRIENSHIPHERE (DONE)
    def get_avatar_url(self, current_user, user):
        if current_user == user:
            return self.mainAvatar()
        elif Follow.objects.filter(follower=current_user, followee=user):
            return self.mainAvatar()
        elif Follow.objects.filter(follower=user, followee=current_user):
            return self.mainAvatar()
        elif Friend.objects.are_friends(current_user, user):
            return self.mainAvatar()
        elif self.user.anonymous:
            return self.anonymousAvatar()
        else:
            return self.mainAvatar()

    def delete(self):
        self.avatar.delete(save=False)
        super().delete()