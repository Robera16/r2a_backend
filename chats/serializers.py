from rest_framework import serializers
from api_auth.models import User
from .models import Group, GroupMessage
from friends.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import APIException


#For groups which are not multitenant get the opposite users data
def get_recepient_user(obj, current_user):
    recepients_list = obj.recepients.all()
    for recepient in recepients_list:
        if recepient != current_user:
            return recepient

class NestedRecepientsSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class GroupSerializer(serializers.ModelSerializer):
    recepients = UserSerializer(many=True, required=False, allow_null = True, read_only=True)
    recepient_ids = NestedRecepientsSerializer(many=True, allow_null=True, write_only=True, required=False)
    recent_messages = serializers.SerializerMethodField()
    group_name = serializers.SerializerMethodField()
    group_avatar = serializers.SerializerMethodField()
    multitenant = serializers.BooleanField(required=True)
    name = serializers.CharField(write_only=True)
    avatar = serializers.ImageField(write_only=True, required=False)

    def get_group_name(self, obj):
        if obj.multitenant:
            return obj.name
        else:
            user_data = get_recepient_user(obj, self.context['request'].user)
            return user_data.first_name
    
    def get_group_avatar(self, obj):
        if obj.multitenant:
            return obj.get_avatar_url()
        else:            
            user_data = get_recepient_user(obj, self.context['request'].user)
            return  user_data.profile.get_avatar_url(current_user=user_data, user=user_data)
    

    def get_recent_messages(self, obj):
        message = GroupMessage.objects.filter(room=obj.id).last()
        return GroupMessageSerializer(message, context = self.context).data

    def create(self, validate_data):
        users = []
        if validate_data['multitenant'] == False and len(validate_data['recepient_ids']) != 1:
            raise  serializers.ValidationError("Single  recepient is required for a non multitenant room")
        if 'recepient_ids' in validate_data:
            recepients_list = validate_data.pop('recepient_ids')
            for recepient in recepients_list:
                users.append(User.objects.get(pk=recepient['id']))
        group = Group.objects.create(**validate_data)
        users.append(self.context['request'].user)
        group.recepients.set(users)
        return group

    def update(self, instance, validate_data):
        instance.name = validate_data.get('name', instance.name)
        instance.description = validate_data.get('description', instance.description)
        instance.avatar = validate_data.get('avatar', instance.avatar)
        if 'recepient_ids' in validate_data:
            users = []
            recepients_list = validate_data.pop('recepient_ids')
            for recepient in recepients_list:
                users.append(User.objects.get(pk=recepient['id']))
                instance.recepients.set(users)
        instance.save()
        return instance

    class Meta:
        model = Group
        fields = '__all__'

class GroupMessageSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    my_message = serializers.SerializerMethodField()

    def get_my_message(self, obj):
        user = self.context['request'].user
        if obj.creator == user:
            return True
        return False

    class Meta:
        model = GroupMessage
        fields = '__all__'
