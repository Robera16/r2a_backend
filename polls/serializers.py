from rest_framework import serializers
from .models import Poll, Choice, PollAnswer, PollComment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'id', 'username']


class ChoiceSerializer(serializers.ModelSerializer):
    answers_count = serializers.SerializerMethodField()
    my_answer = serializers.SerializerMethodField()

    def get_answers_count(self, obj):
        answers = obj.choice_answers
        return answers.count()

    def get_my_answer(self, obj):
        user = self.context['request'].user
        answer = PollAnswer.objects.filter(question=obj.question, user = user, choice=obj).exists()
        return True if answer == 1 else False
    
    class Meta:
        model = Choice
        fields = '__all__'

class PollSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField()
    my_answer =  serializers.SerializerMethodField()
    total_answers_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj):
        return obj.comment.count()

    def get_my_answer(self, obj):
        user = self.context['request'].user
        pollanswer = PollAnswer.objects.filter(question= obj, user = user).first()
        return pollanswer.choice.id if  pollanswer is not None else None


    def get_choices(self, obj):
        pollChoice = ChoiceSerializer(obj.choices, many=True, context=self.context)
        return pollChoice.data
    
    def get_total_answers_count(self, obj):
        answers = PollAnswer.objects.filter(question=obj)
        if answers is not None:
            return answers.count()
        else :
            return 0
    
    class Meta:
        model = Poll
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    my_comment = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_my_comment(self, obj):
        user = self.context['request'].user
        return True if obj.user == user else False
    
    def get_user(self, obj):
        return UserSerializer(obj.user).data
    class Meta:
        model = PollComment
        fields = '__all__'