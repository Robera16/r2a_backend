from rest_framework import serializers
from .models import *
from api_auth.models import UserProfile
User = get_user_model()


class ReelCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReelCommentLike
        fields = '__all__'

class ReelCommentsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user_name = serializers.SerializerMethodField()
    my_comment =  serializers.SerializerMethodField()
    comment_like_count = serializers.SerializerMethodField()

    def get_user_name(self, obj):
        user = User.objects.get(pk=obj.user_id.id)
        return user.username
    
    def get_my_comment(self, obj):
        user  = self.context['request'].user
        myComment = True if obj.user_id == user else False
        return myComment
    
    def get_comment_like_count(self, obj):
        return obj.comment_like.count()

    class Meta:
        model = ReelComments
        fields = '__all__'

class ReelAttachmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReelsAttachment
        fields = '__all__'


class ReelShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReelShares
        fields = '__all__'


class UserReelsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    attachments = ReelAttachmentsSerializer(many=True, allow_null = True, required = False)

    class Meta:
        model = Reel
        fields = '__all__'

class ReelsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    attachments = ReelAttachmentsSerializer(many=True, allow_null = True, required = False)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    shares_count = serializers.SerializerMethodField()
    user_liked_reel = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()
    user_avatar  =  serializers.SerializerMethodField()
    my_post = serializers.SerializerMethodField()
    saved = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_shares_count(self, obj):
        return obj.shares.count()

    def get_user_liked_reel(self, obj):
        user = self.context['request'].user
        likes = ReelLikes.objects.filter(reel_id=obj, user_id=user).count()
        liked = True if likes > 0 else False
        return liked

    def get_user_details(self, obj):
        user = User.objects.get(pk=obj.user_id.id)
        anonymous = user.anonymous 
        return {"first_name": user.first_name, "anonymous": anonymous, "admin": user.admin, "role": user.role, "username": user.username}

    def get_user_avatar(self, obj):
        user_profile = UserProfile.objects.get(user=obj.user_id)
        user = self.context['request'].user
        if user == obj.user_id:
            return user_profile.avatar.url
        else:
            return user_profile.get_avatar_url(current_user = user, user = obj.user_id)

    def get_my_post(self, obj):
        user = self.context['request'].user
        if obj.user_id == user:
            return True
        else:
            return False

    def get_saved(self, obj):
        user = self.context['request'].user
        reels = SavedReel.objects.filter(user_id=user, reel_id=obj).count()
        saved = True if reels > 0 else False
        return saved


    def create(self, validated_data):
        uncleaned_data = self.initial_data
        user = self.context['request'].user

        if "description" not in validated_data and "attachments" not in validated_data:
            raise   serializers.ValidationError("description and attachment required")
        elif "description" in validated_data:
            description = validated_data['description']
            if (description is None or description == "") and  "attachments" not in validated_data:
                raise serializers.ValidationError("description and attachment required")
                

        if 'attachment' in uncleaned_data:
            print('validated data', validated_data)
            attachment = uncleaned_data.pop('attachment')
            file_type = uncleaned_data.pop('file_type')
            reel = Reel.objects.create(**validated_data)
            for attachment, file_type in zip(attachment, file_type):
                attach = ReelsAttachment(reel_id=reel, attachment=attachment, file_type=file_type)
                attach.save()
        else:
            reel = Reel.objects.create(**validated_data)
        return reel
    
    class Meta:
        model = Reel
        fields = '__all__'