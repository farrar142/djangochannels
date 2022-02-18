# chat/routing.py
from django.urls import re_path,path

from chat import consumers as c_c
from trades import consumers as m_c

websocket_urlpatterns = [    
    re_path(r'ws/chat/(?P<room_name>\w+)/$', c_c.ChatConsumer.as_asgi()),
    re_path(r'ws/market/(?P<product_name>\w+)/$', m_c.ProductConsumer.as_asgi()),
    re_path(r'ws/notify/$',c_c.CommonConsumer.as_asgi())
]
ASGI_APPLICATION = "Channels_test_project.routing.application"