# chat/consumers.py
import json
from unidecode import unidecode
from channels.generic.websocket import AsyncWebsocketConsumer
from pprint import pprint
from mysite.serializer import aconverter
from trades.api import get_trade_order
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = u'chat_%s' % unidecode(self.room_name)
        print("connection checker")
        # Join room group
        await self.channel_layer.group_add(
            unidecode(self.room_group_name),
            self.channel_name
        )

        await self.accept()
        await self.send(text_data=json.dumps({
            "result":"succeed"
        })
            
        )
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
    users = {}
    async def connect(self):
        self.room_group_name = 'chat_Notify'
        
        await self.channel_layer.group_add(
            unidecode(self.room_group_name),
            self.channel_name
        )

        await self.accept()
        await self.send_all_trade_order("none")

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
                'type': 'send_all_trade_order',
                'message': 'test1',
                'username': 'test2'
            }
        )

    # Receive message from room group
    async def notify(self, event):
        print("notify")
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'test':'test',
            'message': 'test1',
            'username': 'test2'
        }))#
    async def trade_result(self, event):
        print("trade_result")
        print(event)
        result = {
            'datas':[
                {
                    'market':event['??????'],
                    'amount':event['?????????']
                }
            ]
        }
        await self.send(text_data=json.dumps(result))
        
        
    async def send_all_trade_order(self, event):
        result = {}
        print("?????????/??????????????????")
        try:
            params = await aconverter(await get_trade_order("nothing"))
            print(params)
            result.update(datas = params)
            print("?????????/????????????????????????")
        except:
            print('?????????/????????????????????????')
            pass
        # Send message to WebSocket
        await self.send(text_data=json.dumps(result))
        