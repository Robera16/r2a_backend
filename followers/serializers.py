from rest_framework import serializers
from friendship.models import Follow

from django.contrib.auth import get_user_model 
from api_auth.models import UserProfile
from api_auth.models import District, State, Country

User_Model = get_user_model()
class FollowerslistSerializers(serializers.ModelSerializer):
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

class SearchedChatRoomsList(serializers.Serializer):
    chatRoomId = serializers.CharField()
    first_name = serializers.CharField()
    user_name = serializers.CharField()
    avatar_url = serializers.CharField()
    userId = serializers.CharField()
    tenantId = serializers.CharField()