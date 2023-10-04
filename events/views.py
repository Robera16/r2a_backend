from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from .serializers import EventsSerializer
from .pagination import EventsPagination
from .models import Event

class CreateEvent(APIView):
    permission_classes = (IsAuthenticated, )
    parser_classes = (MultiPartParser, FormParser, FileUploadParser, )

    def post(self, request):
        self.request.POST._mutable = True
        context  = {'request':request} 
        data = request.data
        data['user'] = request.user.id
        serializer = EventsSerializer(data=data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({
            "data": serializer.data
        })
    

class MyEvents(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = EventsSerializer
    pagination_class = EventsPagination
    def get_queryset(self):
        return Event.objects.filter(user = self.request.user).order_by('-created_at')


# TODO: 
# user events (searched user events ) if current user is following  searched user then show all type of events 
# else just show public events only

class EventsForMe(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = EventsSerializer
    pagination_class = EventsPagination
    def get_queryset(self):
        return Event.events_for_me(self.request.user)
