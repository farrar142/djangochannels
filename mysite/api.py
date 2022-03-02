from typing import no_type_check
from django.db import connection
from django.http import HttpResponse, HttpResponseForbidden
from ninja import NinjaAPI,Schema
from ninja.schema import ResolverMetaclass
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.db.models import *
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from pprint import pprint
from unidecode import unidecode
from asgiref.sync import sync_to_async

from accounts.api import accounts_api
from accounts.api import points_api
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
api = NinjaAPI(description=description,csrf=False)

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

@api.post('legacy')
async def legacy(request,form:FormTesT):
    query=f"""
    select * from trade_order
    """
    return HttpResponse("qt")

@database_sync_to_async
def db_connect(query):    
    with connection.cursor() as cursor:
        a = cursor.execute(query)
    return "hehehe"


@api.get('test/ws')
async def websocket_test(request):
    print("here sen messages")
    channel_layer = get_channel_layer()
    print(channel_layer)
    await channel_layer.group_send(
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

@api.post('signin/',url_name="signin")
async def signin(request,user:UserForm=None):
    print(user)
    username = user.username.strip()
    password = user.password.strip()
    token = await login(username,password)
    print(f"로그인 이벤트 발생 // {token}")
    if token:
        return await aconverter(token)
    return HttpResponseForbidden(request)

@database_sync_to_async
def login(username,password):    
    token = ""
    if username and password:
        print(password)
        user = get_user_model().objects.filter(username=username).first()
        if user and check_password(password,user.password):
            token = Token.get_valid_token(user.pk)
    return token
    