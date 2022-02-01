# chat/routing.py
from django.urls import re_path,path

from chat import consumers

websocket_urlpatterns = [    
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/notify/$',consumers.CommonConsumer.as_asgi())
]
ASGI_APPLICATION = "Channels_test_project.routing.application"