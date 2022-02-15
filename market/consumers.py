import json
from django.apps import apps
import django
django.setup()

from django.shortcuts import get_object_or_404
from django.db.models import *
from unidecode import unidecode
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from mysite.serializer import converter

#
class ProductConsumer(AsyncWebsocketConsumer):    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['product_name']
        self.room_group_name = u'product_%s' % unidecode(self.room_name)
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
#
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'update',
                # 'product':product,
                # 'sells':sells,
                # 'buys':buys,
            }
        )
    # Receive message from room group#
    async def update(self, event):
        # product = event['product']
        # sells = event['sells']
        # buys = event['buys']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            # 'product':product,
            # 'sells':sells,
            # 'buys':buys,
            # 'debug':str(self.scope['user']),
            # 'debug2':str(self.channel_layer)
        }))
        