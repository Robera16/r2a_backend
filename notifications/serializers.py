from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Notification
from django.contrib.auth import get_user_model
from api_auth.models import UserProfile
from api.serializers import PostsSerializers

User = get_user_model()

class UserSerializer(ModelSerializer):
    user_avatar = SerializerMethodField()


    def get_user_avatar(self, obj):
        user_profile = UserProfile.objects.get(user=obj.id)
        return user_profile.mainAvatar()
    class Meta:
        model = User
        fields = ['id', 'first_name', 'user_avatar', 'username']

class NotificationSerialier(ModelSerializer):
    cause_user = UserSerializer()
    user = UserSerializer()
    tagged_post = PostsSerializers()
    class Meta:
        model = Notification
        fields = "__all__"