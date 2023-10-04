from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Group, GroupMessage
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from urllib.parse import parse_qs
from .models import Group, GroupMessage
from .serializers import GroupSerializer

@database_sync_to_async
def save_msg(message, user, group_id):
    message = GroupMessage(message=message, creator=user, room=group_id)
    message.save()
    return message.created_at

@database_sync_to_async
def get_room(id):
    room = Group.objects.get(pk=id)
    recepients = room.recepients.all()

    return room, recepients


@database_sync_to_async
def check_user(user, room):
    if user in room.recepients:
        return True
    return False

class ChatsConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        room_id = self.scope['url_route']['kwargs']['group_id']
 
        try:
            if room_id is not None:
                self.room, self.recepients = await get_room(room_id)
                if check_user(self.room, self.user):
                    self.room_group_name = 'chat_%s' % self.room.id
                    await self.channel_layer.group_add(
                        self.room_group_name,
                        self.channel_name
                    )
                    await self.accept()
                else:
                    await self.disconnect(403)
        except Exception as ex:
            print("Some exception")
            raise ex
            await self.disconnect(500)

    async def disconnect(self, close_code):
        #TODO: if user belongs to this group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    async def receive_json(self, data):
        #TODO: add  or self.user.id != data['user_id'] below
        if self.room.id != data['room_id']:
            await self.disconnect(403)
    
        message_type = data['message_type']
        if message_type == "text":
            message = data['message']
            time = await save_msg(message, self.user, self.room)
            time = time.strftime("%d %b %Y %H:%M:%S %Z")
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_to_websocket',
                    'message_type': 'text',
                    'message': message,
                    'sender': self.user.first_name,
                    'room_id': self.room.id,
                    'created': time,
                }
            )
    async def send_to_websocket(self, event):
        await self.send_json(event)

class SocketCostumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):
        print(self.scope['user'])
        await self.send({
            "type": "websocket.send",
            "text": event['text'],
        })

    async def websocket_disconnect(self, event):
        await self.send({
            "type": "websocket.close"
        })