# chat/consumers.py
import json
from unidecode import unidecode
from channels.generic.websocket import AsyncWebsocketConsumer
from pprint import pprint
from mysite.functions import debug

from trades.api import get_trade_order
class PersonalConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['token']
        print("personal 연결요청")
        self.room_group_name = u'personal_%s' % unidecode(self.room_name)
        debug(self.scope)
        print("connection checker")
        # Join room group
        await self.channel_layer.group_add(
            unidecode(self.room_group_name),
            self.channel_name
        )

        await self.accept()
        await self.send(text_data=json.dumps({
            "result":"personal채널 연결성공",
            "message":f"{self.room_group_name}에 연결됨"
            })            
        )
        await self.receive('tet')
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat',
            }
        )

    # Receive message from room group
    async def chat(self, event):

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'result':f"Echoing from PersonalChannel {self.room_group_name}"
        }))