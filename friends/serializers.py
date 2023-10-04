from rest_framework import serializers

# this is just .models.User which is set a deafult user model for this project so we can directly import it from django
from django.contrib.auth import get_user_model 
from api_auth.models import UserProfile

User_Model = get_user_model()
from friendship.models import Friend, Follow, Block, FriendshipRequest
from api_auth.serializers import ProfileSerializers
from api_auth.models import District, State, Country

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializers()
    constituency_details = serializers.SerializerMethodField()

    def get_constituency_details(self, obj):
        return None

    class Meta:
        model = User_Model
        exclude = ['password', 'last_login', 'otp', 'staff', 'constituency_id', 'created_at', 'updated_at']

class FriendsRequestListSerializers(serializers.ModelSerializer):
    from_user = UserSerializer()
    to_user = UserSerializer()
    class Meta:
        model = FriendshipRequest
        fields = '__all__'

class FriendsListSerializers(serializers.ModelSerializer):
    user_avatar  =  serializers.SerializerMethodField()
    constituency_details = serializers.SerializerMethodField()

    def get_constituency_details(self, obj):
        return None
    
    
    def get_user_avatar(self, obj):
        user_profile = UserProfile.objects.get(user=obj.id)
        return user_profile.get_avatar_url(current_user = self.context['request'].user, user = obj)

    class Meta:
        model = User_Model
        fields = ['first_name', 'last_name', 'anonymous', 'constituency_details',  'user_avatar', 'id', 'username'] 