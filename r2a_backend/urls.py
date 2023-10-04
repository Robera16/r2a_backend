"""r2a_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

admin.site.site_url = None
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('api_auth.urls')),
    path('api/friends/', include('friends.urls')),
    path('api/chats/', include('chats.urls')),
    path('api/support/', include('support.urls')),
    path('api/stories/', include('stories.urls')),
    path('api/', include('api.urls')),
    path('polls/', include('polls.urls')),
    path('api/followers/', include('followers.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/events/', include('events.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)