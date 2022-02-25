from django.db import connection
from django.shortcuts import render
from ninja import NinjaAPI,Form,Schema
from django.db.models import *
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from pprint import pprint
from unidecode import unidecode


from accounts.api import accounts_api
from accounts.api import points_api
from assets.api import router as assets_api
from stocks.api import router as products_api
from trades.api import router as trades_api


from mysite.serializer import converter
from commons.const import *
from stocks.models import *
from trades.models import * 
from accounts.models import *
from assets.models import *
from commons.models import *
from trades.logics import *
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
##all(),get() == lazy loading
##get() == eager loading
@api.get('legacy')
async def legacy(request):
    query=f"""
    select * from trade_order
    """
    return await db_connect(query)

@database_sync_to_async
def db_connect(query):    
    with connection.cursor() as cursor:
        a = cursor.execute(query)
    return dir(a)


@api.get('test/ws')
async def websocket_test(request):
    
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        unidecode('chat_Notify'),
        {
            "type":"notify",
            "result":"succeed",
        }
    )

async def schema_by_model_name(form_dict:dict,model_name:str,getter_func:Func):
    """
    form_dict = SCHEMA.dict()
    """
    _model_name= form_dict[model_name]
    model = await getter_func(_model_name)
    form_dict.pop(model_name)
    attr = {f'{type(model).__name__}'.lower():model}
    form_dict.update(attr)
    return form_dict