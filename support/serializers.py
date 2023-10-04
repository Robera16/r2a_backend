from rest_framework import serializers
from api_auth.models import User
from .models import AdminTicket, SupportTicket


class AdminTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdminTicket
        fields = '__all__'

class SupportTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupportTicket
        fields = '__all__'