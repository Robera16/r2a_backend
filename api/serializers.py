from rest_framework import serializers
from .models import Post, Attachment, Likes, Comments, SavedPost
from django.contrib.auth import get_user_model
from api_auth.models import UserProfile
User = get_user_model()
from api_auth.serializers import ProfileSerializers, ConstituencySerializers
from api_auth.models import Constituency, State, Country, District
from friendship.models import Friend, FriendshipRequest, Follow
import json
import re

class AttachmentsSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Attachment
        fields = ['attachment', 'id', 'file_type']

class SingleAttachmentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Attachment
        fields = '__all__'

#this for update comment the below serializer is not working for both update  and also for POSTS so used this instead
#TODO: investiage the above reason
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.message = validated_data.get('message', instance.message)
        instance.save()
        return instance


class CommentsSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user_name = serializers.SerializerMethodField()
    my_comment =  serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()

    def get_user_name(self, obj):
        user = User.objects.get(pk=obj.user_id.id)
        return user.username
    
    def get_first_name(self, obj):
        user = User.objects.get(pk=obj.user_id.id)
        return user.first_name

    def get_my_comment(self, obj):
        user  = self.context['request'].user
        myComment = True if obj.user_id == user else False
        return myComment
    class Meta:
        model = Comments
        fields = '__all__'

class TaggedUserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    def get_avatar(self, obj):
        user_profile = UserProfile.objects.get(user=obj.id)
        return user_profile.get_avatar_url(current_user = obj, user = obj)
    class Meta:
        model = User
        fields = ['avatar', 'id', 'first_name', 'username']


class PostsSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    attachments = AttachmentsSerializers(many=True, allow_null = True, required = False)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    user_liked_post = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()
    user_avatar  =  serializers.SerializerMethodField()
    constituency_details = serializers.SerializerMethodField()
    district_details = serializers.SerializerMethodField()
    my_constituency_post = serializers.SerializerMethodField()
    my_post = serializers.SerializerMethodField()
    my_district_post = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    tagged_users = TaggedUserSerializer(many=True, required=False, read_only=True)
    tagged_user_ids = serializers.ListField(write_only=True, required=False)
    saved = serializers.SerializerMethodField()
    saved_count = serializers.SerializerMethodField()

    def get_country(self, obj):
        user = obj.user_id
        if user.country:
            return user.country.name
    def get_saved(self, obj):
        user = self.context['request'].user
        posts = SavedPost.objects.filter(user=user, post=obj).count()
        saved = True if posts > 0 else False
        return saved

    def get_saved_count(self, obj):
        return obj.saved.count()

    def get_user_avatar(self, obj):
        user_profile = UserProfile.objects.get(user=obj.user_id)
        user = self.context['request'].user
        if user == obj.user_id:
            return user_profile.avatar.url
        else:
            return user_profile.get_avatar_url(current_user = user, user = obj.user_id)

    def get_user_details(self, obj):
        user = User.objects.get(pk=obj.user_id.id)
        anonymous = user.anonymous 
        return {"first_name": user.first_name, "anonymous": anonymous, "admin": user.admin, "role": user.role, "username": user.username}

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_user_liked_post(self, obj):
        user = self.context['request'].user
        likes = Likes.objects.filter(post_id=obj, user_id=user).count()
        liked = True if likes > 0 else False
        return liked
    # TODO: remove this on later point as user does not have this jazz any more 
    def get_constituency_details(self, obj):
        return None
    
        # TODO: remove this on later point as user does not have this jazz any more 
    def get_district_details(self, obj):
        return None

    # TODO: remove this on later point as user does not have this jazz any more 
    def get_my_constituency_post(self, obj):
        return False
    
    def get_my_post(self, obj):
        user = self.context['request'].user
        if obj.user_id == user:
            return True
        else:
            return False
    # TODO: remove this on later point as user does not have this jazz any more 
    def get_my_district_post(self, obj):
        return False

    def create(self, validated_data):
        uncleaned_data = self.initial_data

        print('I am creating', validated_data)
        print('uncleanded data', uncleaned_data)
        user = self.context['request'].user
        tagged_user_ids_list = []

        if "description" not in validated_data and "attachments" not in validated_data:
            raise   serializers.ValidationError("Either description or media are require")
        elif "description" in validated_data:
            description = validated_data['description']
            if (description is None or description == "") and  "attachments" not in validated_data:
                raise serializers.ValidationError("Either description or media are require")
                
        if 'tagged_user_ids' in validated_data:
            # print('tagged_user_ids', validated_data)
            ids = validated_data.pop('tagged_user_ids')

            integer_ids = [int(num) for num in re.findall(r'\d+', str(ids))]

            # print('ids', ids, "intergers", integer_ids)
            try: 
                tagged_user_ids_list = integer_ids
            except Exception as e:
                print("Problem while tagging users passed ")
                print(ids)
                print(e)

        print('validated_data', validated_data)
        if 'attachments' in validated_data:
            print('validated data', validated_data)
            attachments = validated_data.pop('attachments')
            post = Post.objects.create(**validated_data)
            for attachment in attachments:
                Attachment.objects.create(post_id=post, **attachment)
        else:
            print('no attachment')
            post = Post.objects.create(**validated_data)
        for user in tagged_user_ids_list:
            user_obj = User.objects.get(pk=int(user))
            post.tagged_users.add(user_obj)
        return post

    def update(self, instance, validated_data):
        if "description" not in validated_data and "attachments" not in validated_data:
            raise   serializers.ValidationError("Either description or media are require")
        elif "description" in validated_data:
            description = validated_data['description']
            if (description is None or description == "") and  "attachments" not in validated_data:
                raise serializers.ValidationError("Either description or media are require")

        instance.description = validated_data.get('description', instance.description)
        instance.gps_data = validated_data.get('gps_data', instance.gps_data)
        instance.category = validated_data.get('category', instance.category)
        instance.district = validated_data.get('district', instance.district)
        instance.save()
        tagged_user_list = []
        if 'tagged_user_ids' in validated_data:
            tagged_user_ids_list = []
            ids = validated_data.pop('tagged_user_ids')
            try: 
                tagged_user_ids_list = json.loads(ids[0])
            except Exception as e:
                print("Problem while tagging users passed ")
                print(ids)
                print(e)

            for id in tagged_user_ids_list:
                user = User.objects.get(pk=int(id))
                tagged_user_list.append(user)
        if 'attachments' in validated_data:
            attachments = validated_data.pop('attachments')
            for attachment in attachments:
                if not "file_type" in attachment or not "attachment" in attachment:
                    raise serializers.ValidationError("File type and attachment both are mandatory")
                Attachment.objects.create(post_id = instance, **attachment)
        instance.tagged_users.set(tagged_user_list)
        return instance
    
    #TODO: remove this as well we only will post category 4 posts (news fees) 1, 2 can be removed later
    def validate_data(self, data):
        if(data['category'] == 2 and data.get('district') == None):
            return False
        elif (data['category'] == 1 and self.context['request'].user.constituency_id == None):
            return False
        else:
            return True

    # TODO: we can remove this validation alltogether
    def validate(self, data):
        if not self.validate_data(data):
            raise serializers.ValidationError("District or constituency are mandatory for post creation")
        return data
    class Meta:
        model = Post
        fields = '__all__'

class UsersListSerializers(serializers.ModelSerializer):
    user_avatar  =  serializers.SerializerMethodField()
    constituency_details = serializers.SerializerMethodField()
    #this is kept here so as to make older versions usable
    are_friends =  serializers.SerializerMethodField()
    #check if current follows the opposite
    follows = serializers.SerializerMethodField()
    #check if current user following opposite
    follower = serializers.SerializerMethodField()
    #Get all followers count of oposite user
    followers_count = serializers.SerializerMethodField()
    #Get all following count of opposite user
    followings_count = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()

    def get_followers_count(self, obj):
        user = obj
        return len(Follow.objects.followers(user=user))

    def get_country(self, obj):
        if obj.country:
            return obj.country.name

    def get_followings_count(self, obj):
        user = obj
        return len(Follow.objects.following(user=user))

    def get_follows(self, obj):
        user = obj
        current_user =  self.context['request'].user
        return Follow.objects.follows(follower=current_user, followee=user)
    
    def get_follower(self, obj):
        user = obj
        current_user =  self.context['request'].user
        return Follow.objects.follows(follower=user, followee=current_user)
    
    # TODO: remove this on later point as user does not have this jazz any more 
    def get_constituency_details(self, obj):
        return None
    
    def get_are_friends(self, obj):
        user = obj
        current_user =  self.context['request'].user
        return Friend.objects.are_friends(user, current_user)
    
    #need to chnage this at model level
    def get_user_avatar(self, obj):
        current_user =  self.context['request'].user
        user_profile = UserProfile.objects.get(user=obj.id)
        return user_profile.get_avatar_url(current_user = current_user, user = obj)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'anonymous', 'constituency_details', 'user_avatar', 'admin', 
                  'are_friends', 'email', 'role', 'follows', 'follower', 'followers_count', 'followings_count', 'country', 'username']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UsersSerializers(serializers.ModelSerializer):
    profile = ProfileSerializer()
    #TODO: backward compatability
    are_friends =  serializers.SerializerMethodField()
    constituency_details = serializers.SerializerMethodField()
    #TODO: backward compatability
    request_sent =  serializers.SerializerMethodField()
    user_avatar = serializers.SerializerMethodField()
    follows = serializers.SerializerMethodField()
    follower = serializers.SerializerMethodField()
    #Get all followers count of oposite user
    followers_count = serializers.SerializerMethodField()
    #Get all following count of opposite user
    followings_count = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    
    def get_country(self, obj):
        if obj.country:
            return obj.country.name

    #check if current follows the opposite
    def get_follows(self, obj):
        user = obj
        current_user =  self.context['request'].user
        return Follow.objects.follows(follower=current_user, followee=user)

    #check if current user following opposite
    def get_follower(self, obj):
        user = obj
        current_user =  self.context['request'].user
        return Follow.objects.follows(follower=user, followee=current_user)

    def get_followers_count(self, obj):
        user = obj
        return len(Follow.objects.followers(user=user))
    
    def get_followings_count(self, obj):
        user = obj
        return len(Follow.objects.following(user=user))


    def get_are_friends(self, obj):
        user = obj
        current_user =  self.context['request'].user
        return Friend.objects.are_friends(user, current_user)
    
    #@FRIENSHIPHERE (DONE)
    def get_request_sent(self, obj):
        # user = obj
        # current_user = self.context['request'].user
        # if Friend.objects.can_request_send( current_user, user):
        #     request_id = FriendshipRequest.objects.get(from_user = current_user, to_user = user).id
        #     return {"sent_by": "me", "request_id": request_id, "can_create": False}
        # elif Friend.objects.can_request_send(user, current_user):
        #     request_id = FriendshipRequest.objects.get(from_user = user, to_user = current_user).id
        #     return {"sent_by": "other", "request_id": request_id, "can_create": False}
        # else:
        return {"sent_by": None , "request_id": None, "can_create": True}

    def get_user_avatar(self, obj):
        current_user =  self.context['request'].user
        user_profile = UserProfile.objects.get(user=obj.id)
        return user_profile.get_avatar_url(current_user = current_user, user = obj)

    # TODO: remove this on later point as user does not have this jazz any more 
    def get_constituency_details(self, obj):
        return None


    def update(self, instance, validated_data):
        profile = instance.profile
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.anonymous = validated_data.get('anonymous', instance.anonymous)
        if validated_data.get("profile"):
            profile_data = validated_data.get('profile')
            profile.avatar = profile_data.get("avatar", profile.avatar) 
            profile.banner = profile_data.get("banner", profile.banner)
            profile.location = profile_data.get("location", profile.location)
            profile.sex = profile_data.get("sex", profile.sex)
            profile.dob = profile_data.get("dob", profile.dob)
            profile.bio = profile_data.get("bio", profile.bio)
            profile.save()           
        instance.save()
        return instance

    class Meta:
        model = User
        exclude = ['last_login', 'password', 'created_at', 'updated_at', 'otp']


          