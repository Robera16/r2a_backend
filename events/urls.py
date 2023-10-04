from django.urls import path
from .views import CreateEvent, MyEvents, EventsForMe

urlpatterns = [
    path('new/', CreateEvent.as_view()),
    path('my_events/', MyEvents.as_view()),
    path('for_me/', EventsForMe.as_view())
]