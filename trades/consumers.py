import json
from django.apps import apps
import django
django.setup()

from pprint import pprint

from django.shortcuts import get_object_or_404
from django.db.models import *
from unidecode import unidecode
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from mysite.serializer import converter
from trades.api import *
#
class ProductConsumer(AsyncWebsocketConsumer):    
    async def connect(self):
        
        self.room_name = self.scope['url_route']['kwargs']['product_name']
        self.room_group_name = u'product_%s' % unidecode(self.room_name)
        pprint(self)
        #pprint(self.scope)
        # Join room group
        await self.channel_layer.group_add(
            unidecode(self.room_group_name),
            self.channel_name
        )
        await self.accept()
        print("==connected==")
        await self.send(text_data=json.dumps({
            "result":"connected",
            'datas':None,
        }))
        print("===welcome message send====")
        for i in self.scope['headers']:
            if i[0] == b'origin':
                print(i)
        
    async def disconnect(self, close_code):
        # Leave room group
        print("====leaves====")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
#
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print("===debugg====")
        print(text_data_json)
        result={'type':'update'}
        # try:
        #     if text_data_json['action'] == "get_trades":
        #         result.update(context = get_trade_order("nothing"))
        # except:
        #     pass
        await self.channel_layer.group_send(
            self.room_group_name,
            result
        )
    # Receive message from room group#
    async def update(self, event):
        # product = event['product']
        # sells = event['sells']
        # buys = event['buys']
        result = {"result":"succeed"}
        try:
            params = await get_trade_order("nothing")
            params = params.get('datas')
            result.update(datas = params)
        except:
            pass
        # Send message to WebSocket
        await self.send(text_data=json.dumps(result))
        
        
        