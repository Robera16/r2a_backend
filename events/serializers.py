from rest_framework import serializers
from .models import Event
from api.serializers import UsersSerializers

class EventsSerializer(serializers.ModelSerializer):
    user = UsersSerializers(read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        event = Event.objects.create(**validated_data)
        return event
    
    class Meta:
        model = Event
        fields = '__all__'