# chat/consumers.py
# import json

# from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()

# class ChatsConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         # self.room_group_name = f"chat_{self.room_name}"

#         # # Join room group
#         # await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         self.user_name = self.scope["url_route"]["kwargs"]["username"]
#         self.group_id = self.scope["url_route"]["kwargs"]["group_id"]
#         print('user', self.room_name, 'group', self.group_id)
#         # other_user =await sync_to_async(User.objects.get)(username='workneh')
#         # print('other', other_user.username)

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name, {"type": "chat.message", "message": message}
#         )

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event["message"]

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({"message": message}))



from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Group, GroupMessage
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from urllib.parse import parse_qs
from .models import Group, GroupMessage, OneToOneChat
from .serializers import GroupSerializer

@database_sync_to_async
def save_msg(message, user, group_id):
    message = GroupMessage(message=message, creator=user, room=group_id)
    message.save()
    return message.created_at

@database_sync_to_async
def save_one_to_one_msg(message, sender, recipient):
    message = OneToOneChat(message=message, sender=sender, recipient=recipient)
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
        # self.user = self.scope['user']
        self.user = self.scope["url_route"]["kwargs"]["username"]
        room_id = self.scope["url_route"]["kwargs"]["group_id"]
 
        try:
            if room_id is not None:
                self.room, self.recepients = await get_room(room_id)
                # print('self.room', self.room, 'self.user', self.user)
                
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

            sending_user =await sync_to_async(User.objects.get)(username=self.user)

            time = await save_msg(message, sending_user, self.room)
            time = time.strftime("%d %b %Y %H:%M:%S %Z")
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_to_websocket',
                    'message_type': 'text',
                    'message': message,
                    'sender': self.user,
                    'room_id': self.room.id,
                    'created': time,
                }
            )
    async def send_to_websocket(self, event):
        await self.send_json(event)



class OneToOneChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = self.scope["url_route"]["kwargs"]["username"]
        other_user_id = self.scope["url_route"]["kwargs"]["user_id"]
        # other_user = User.objects.get(id=other_user_id)  # Fetch the other user
        self.one_to_one_group_name = 'chat_%s_%s' % (self.user, other_user_id)

        # print("one to one", self.one_to_one_group_name)
        await self.channel_layer.group_add(self.one_to_one_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.one_to_one_group_name, self.channel_name)

    async def receive_json(self, data):
        message_type = data['message_type']
        message = data['message']

        if message_type == "text" and message:
            # Handle text messages
            # sender = self.user
            sender =await sync_to_async(User.objects.get)(username=self.user)
            recipient_id = data['recipient_id']  # Ensure you include the recipient's ID in the JSON data

            if recipient_id:
                try:
                    recipient =await sync_to_async(User.objects.get)(id=recipient_id)
                    # recipient = User.objects.get(id=recipient_id)
                except User.DoesNotExist:
                    # Handle the case where the recipient does not exist
                    return

                # Save the message to the database
                time = await save_one_to_one_msg(message, sender, recipient)

                # Prepare the message for sending
                time = time.strftime("%d %b %Y %H:%M:%S %Z")

                # Send the message to the recipient's WebSocket
                await self.channel_layer.group_send(
                    self.one_to_one_group_name, 
                    {
                        'type': 'send_to_websocket',
                        'message_type': 'text',
                        'message': message,
                        'sender': self.user,
                        'recipient_id': recipient_id,
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