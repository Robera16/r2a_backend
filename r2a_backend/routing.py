from django.urls import path

from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from chats.consumer import SocketCostumer, ChatsConsumer
from chats.token_auth import TokenAuthMiddlewareStack

# application = ProtocolTypeRouter({
#     "websocket": TokenAuthMiddlewareStack(
#         URLRouter([
#             path("channel/socket/", SocketCostumer),
#             path("channel/group_chat/<int:group_id>/", ChatsConsumer),
#         ]),
#     ),

# })

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("channel/socket/", SocketCostumer),
        path("channel/group_chat/<int:group_id>/", ChatsConsumer),
    ]),
})
