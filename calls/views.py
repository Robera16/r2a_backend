from django.http import JsonResponse
from twilio.twiml.voice_response import VoiceResponse

from django.conf import settings
from twilio.rest import Client

from rest_framework.decorators import api_view, permission_classes

# Twilio setup
TWILIO_ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


@api_view(['POST'])
def make_call(request):
   

    return JsonResponse({'twiml': 'hello'})
