import json
import orjson
from django.db import connection
from django.http import HttpResponse, HttpResponseForbidden
from ninja import NinjaAPI,Schema
from ninja.renderers import BaseRenderer
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.db.models import *
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from unidecode import unidecode

from accounts.api import accounts_api
from assets.api import router as assets_api
from stocks.api import router as products_api
from trades.api import router as trades_api

from mysite.functions import debug
from mysite.serializer import aconverter
from commons.const import *
from stocks.models import *
from trades.models import * 
from accounts.models import *
from assets.models import *
from commons.models import *
from trades.logics import *
from custommiddle.models import *
from stocks.tasks import *
description="""
# 모의 주식 투자 시뮬레이터 API DOCS\n
### RESULT EX\n
    'json' : {\n
        'system':{\n
            'result' : 'SUCCEED' or 'FAILED'\n
        },\n
        'datas':[\n
            {'data1':'value1'},\n
            {'data2':'value2'},\n
        ],\n
    }\n
    
    CONST:
        SUCCEED = "SUCCEED"
        FAILED = "FAILED"
        NONE = "NONE"

        BUY = 1
        SELL = 2

        NORMAL = 1
        COMPLETE = 2
        CANCELED = 3
"""
class MyRenderer(BaseRenderer):
    media_type = "application/json"
    
    def render(self,request,data,*,response_status):
        if data:
            return json.dumps(converter(data))
        else:
            return json.dumps({'message':'none'})

api = NinjaAPI(description=description,csrf=False,renderer=MyRenderer())

api.add_router('/accounts/',accounts_api)
api.add_router('/assets/',assets_api)
api.add_router('/products/',products_api)
api.add_router('/trades/',trades_api)

##all(),filter() == lazy loading
##get() == eager loading
        
class FormTesT(Schema):
    line1:str
    line2:int
    line3:str
    
@sync_to_async
@api.get('celery/')
def celery(request):
    logging_product.delay().get()
    return HttpResponse("celery")

@sync_to_async
@api.post('legacy')
def legacy(request,form:FormTesT):
    query=f"""
    select * from trade_order
    """
    return HttpResponse("qt")


@sync_to_async
@api.get('test/ws')
def websocket_test(request):
    print("here sen messages")
    channel_layer = get_channel_layer()
    print(channel_layer)
    async_to_sync(channel_layer.group_send)(
        unidecode('chat_Notify'),
        {
            "type":"send_all_trade_order",
                'message': 'test1',
                'username': 'test2'
        }
    )
    print("done?")
class UserForm(Schema):
    username:str=""
    password:str=""

@sync_to_async
@api.post('signin/',url_name="signin")
def signin(request,user:UserForm=None):
    print(user)
    username = user.username.strip()
    password = user.password.strip()
    token = login(username,password)
    print(f"로그인 이벤트 발생 // {token}")
    if token:
        return token
    return HttpResponseForbidden(request)

def login(username,password):    
    token = ""
    if username and password:
        print(password)
        user = get_user_model().objects.filter(username=username).first()
        if user and check_password(password,user.password):
            token = Token.get_valid_token(user.pk)
    return token
    