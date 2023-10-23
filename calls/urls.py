from django.urls import path
from .views import *

urlpatterns = [
    path('make_call/', make_call, name='make_call'),
]