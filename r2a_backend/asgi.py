"""
ASGI config for r2a_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

# mysite/asgi.py
import django
django.setup()

import os

from channels.routing import ProtocolTypeRouter
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from chats.routing import websocket_urlpatterns
from channels.security.websocket import AllowedHostsOriginValidator


from channels.auth import AuthMiddlewareStack

django_asgi_app = get_asgi_application()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'r2a_backend.settings')



application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket":AllowedHostsOriginValidator(AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
    )
    )
})