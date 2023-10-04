from rest_framework import serializers
from .models import Story
from django.contrib.auth import get_user_model
from api_auth.models import UserProfile
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UsersListSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    stories_count = serializers.SerializerMethodField()
    mine = serializers.SerializerMethodField()
    seen_all = serializers.SerializerMethodField()

    """
        return True if current user has seen all stories of other user, if current user is same as other user it returns true

        (1) count all the stories the oppisite user has
        (2) count all the stories in which current user in (has seen) (stories.seen_by) 
        if 1 and 2 are equal that means current user has seen all stories for opposite user the return True else False
    """
    def get_seen_all(self, obj):
        current_user  = self.context['request'].user
        if obj  == current_user:
            return True
        stories_count = User.objects.get(pk=obj.id).stories.count()
        seen_by = User.objects.get(pk=obj.id).stories.filter(seen_by__in = User.objects.filter(pk=current_user.id)).count()      
        if seen_by == stories_count:
            return True
        else:
            return False

    def get_stories_count(self, obj):
        return obj.stories.count()

    def get_avatar(self, obj):
        profile =  UserProfile.objects.get(user=obj)
        return profile.mainAvatar()

    def get_mine(self, obj):
        current_user  = self.context['request'].user
        if obj == current_user:
            return True
        return False

    class Meta:
        model = User
        fields = ['first_name', 'id', 'avatar', 'stories_count', 'mine', 'seen_all', 'created_at', 'updated_at', 'username']

class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        profile =  UserProfile.objects.get(user=obj)
        return profile.mainAvatar()
    class Meta:
        model = User
        fields = ['first_name', 'id', 'avatar', 'username']

class StoriesListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    seen_by = UserSerializer(many=True, read_only=True)
    my_story = serializers.SerializerMethodField()
    seen = serializers.SerializerMethodField()


    def get_my_story(self, obj):
        current_user  = self.context['request'].user
        if obj.user == current_user:
            return True
        return False

    def get_seen(self, obj):
        current_user  = self.context['request'].user
        if current_user in obj.seen_by.all():
            return True
        return False
    class Meta:
        model = Story
        fields = '__all__'

class MyStroriesSerialier(serializers.ModelSerializer):
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        if "seen_by" in validated_data: validated_data.pop("seen_by")
        if(validated_data['media_type'] == 1 or validated_data['media_type'] == 2):
            if "file" not in validated_data:
                raise ValidationError("file is required for Media type stories")
            elif(validated_data['file'] == None or validated_data['file']  == ''):
                raise ValidationError("file is required for Media type stories")
        elif(validated_data['media_type'] == 3):
            if "text" not in validated_data:
                raise ValidationError("text is required for Text type stories")
            elif(validated_data['text'] == None or validated_data['text']  == ''):
                raise ValidationError("text is required for Text type stories")
        elif(validated_data['media_type'] == 4):
            raise ValidationError("Cannot create a un-supported strory type")
        story = Story.objects.create(**validated_data)
        return story

    class Meta:
        model = Story
        fields = '__all__'


 
