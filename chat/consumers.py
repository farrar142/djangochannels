# chat/consumers.py
import json
from unidecode import unidecode
from channels.generic.websocket import AsyncWebsocketConsumer
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = u'chat_%s' % unidecode(self.room_name)
        # Join room group
        await self.channel_layer.group_add(
            unidecode(self.room_group_name),
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat',
                'message': message,
                'username': username
            }
        )

    # Receive message from room group
    async def chat(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'author':username,
            'message': message,
            'debug':str(self.scope['user']),
            'debug2':str(self.channel_layer)
        }))
        
class CommonConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_Notify'
        # Join room group
        await self.channel_layer.group_add(
            unidecode(self.room_group_name),
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        # username = text_data_json['username']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'notify',
                'message': 'test1',
                'username': 'test2'
            }
        )

    # Receive message from room group
    async def notify(self, event):

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'test':'test'
        }))