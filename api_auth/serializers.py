from rest_framework import serializers
from django.contrib.auth import get_user_model # this is just .models.User which is set a deafult user model for this project so we can directly import it from django
User_Model = get_user_model()
from .models import State, District, Constituency, UserProfile, Country, PhoneOtp
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import APIException


class PhoneOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneOtp
        fields = ['country', 'phone_number']

class APIException401(APIException):
    status_code = 401
    # The Below code is to ovveride the default deatil to custom message if needed when we throw and exception
    # def __init__(self, detail, status_code=None):
    #     self.detail = {"message": "Admin cannot Login to mobile app"}
    #     if status_code is not None:
    #         self.status_code = status_code

class SingInSerializer(TokenObtainPairSerializer):
    #TODO implement Allow Active accounts to login 
    def validate(self, attrs):
        data = super().validate(attrs)
        if (self.user.admin):
           raise APIException401('Admin Cannot login on Mobile App')
        else:
            refresh = self.get_token(self.user)
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            data['first_name'] = self.user.first_name
            data['last_name'] = self.user.last_name
            data['email'] = self.user.email
            data['phone_number'] = self.user.phone_number
            data['id'] = self.user.id
            data['avatar_url'] = self.user.profile.avatar.url
            data['can_create'] = self.user.can_create
            data['role'] = self.user.role
            data['is_admin'] = self.user.admin 
            data['foreign_user'] = self.user.foreign_user
            data['username'] = self.user.username
            return data


class UserProfileSerializers(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        return obj.avatar.url
    class Meta:
        model = UserProfile
        fields = '__all__'

"""
    For registartion
"""
class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializers(read_only=True)
    password = serializers.CharField(write_only = True)
    def create(self, validate_data):
        
        user = User_Model.objects.create_user(
            username = validate_data['username'],
            phone_number = validate_data['phone_number'],
            password = validate_data['password'],
            first_name = validate_data['first_name'],
            email = validate_data['email'],
            last_name = validate_data['last_name'],
            foreign_user = validate_data['foreign_user'],
            country = validate_data['country']
        )
        return user

    class Meta:
        model = User_Model
        fields = '__all__'
        # exclude = ['last_name', 'email']

class StateSerializers(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class CountrySerializers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class DistrictSerializers(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class ConstituencySerializers(serializers.ModelSerializer):
    class Meta:
        model = Constituency
        fields = '__all__'

class ProfileSerializers(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        user = self.context['request'].user
        if user == obj.user:
            return obj.avatar.url
        else:
            return obj.get_avatar_url(current_user = user, user = obj.user)
    class Meta:
        model = UserProfile
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    model = User_Model
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)