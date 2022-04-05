# chat/routing.py
from django.urls import re_path,path

from accounts import consumers as a_c
from chat import consumers as c_c
from stocks import consumers as s_c

websocket_urlpatterns = [    
    re_path(r'ws/personal/(?P<token>\w+)/$', a_c.PersonalConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', c_c.ChatConsumer.as_asgi()),
    re_path(r'ws/price/(?P<product_id>\w+)/$', s_c.PriceConsumer.as_asgi()),
    re_path(r'ws/notify/$',c_c.CommonConsumer.as_asgi())
]
ASGI_APPLICATION = "Channels_test_project.routing.application"