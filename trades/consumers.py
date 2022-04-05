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
        
        