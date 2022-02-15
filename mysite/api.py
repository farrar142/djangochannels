from ninja import NinjaAPI,Form,Schema
from django.db.models import *
from channels.db import database_sync_to_async
from pprint import pprint

from mysite.serializer import converter
from mysite.const import *
from products.models import *
from market.models import *
from accounts.models import *
from commons.models import *
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
##all(),get() == lazy loading
##get() == eager loading
class ProductForm(Schema):
    name : str
    category_id : int
    
class TradeOrderForm(Schema):
    asset_id : int
    point : int
    quantity : int
    type_id : int
    

@api.get('/products')
async def get_product_all(request):
    result = Product.objects.all()#db에 query하지않음
    return await converter(result)

@api.get('/product/get/{product_id}')
async def get_product(request,product_id:int):
    result = Product.objects.filter(**{"pk":product_id})
    return await converter(result)

@api.post('/product/post/')
async def post_product(request,form:ProductForm):
    """
    product_id : int
    user_id : int
    price : int
    quantity : int
    type_id : int
    code_id : int
    """
    result = Product(**form.dict())
    await result.async_save()
    return await converter(result)
@api.get('/asset/get')
async def get_asset(request,product_id,user_id):
    try:
        result = await Asset.get_asset(user_id,product_id)
    except:
        result = fail_message("user 혹은 product가 존재하지 않습니다.")
    return await converter(result)

@api.get('/tradeOrders')
async def get_tradeOrder(
    request,asset_id:int=0,product_id:int=0,
    user_id:int=0,type_id=0,code_id=0,trade_item_code_id:int=0
    ):
    """
    ?user_id=   1 -> 1번유저의 거래기록 반환
    
    ?type_id=   1 -> BUY기록
                2 -> SELL기록
    
    ?code_id=   1 -> NORMAL기록
                2 -> COMPLETE기록
                3 -> CANCELED기록
    
    """
    result = TradeOrder.objects.prefetch_related('tradeitem').annotate(
        product_id=F('asset__product__id'),
        product_name=F('asset__product__name'),
        user_id=F('asset__user__id'),
        user_name=F('asset__user__username'),
        type_name=F('type__type'),
        trade_amount=Count('tradeitem'),
        point=F('tradeitem__point'),
        trade_item_code_id=F('tradeitem__code__id')
    )
    #await aprint(result.query)
    #return await converter(result)
    ##tradeitem의 상태를 판별해서 카운트해야됨.
    if asset_id >= 1:
        result = result.filter(asset_id=asset_id)
    if product_id >= 1:
        result = result.filter(product_id=product_id)
    if user_id >= 1:
        result = result.filter(user_id=user_id)
    if type_id >= 1:
        result = result.filter(type_id=type_id)
    if code_id >= 1:
        result = result.filter(code_id=code_id)
    if trade_item_code_id >= 1:
        result = result.filter(trade_item_code_id=trade_item_code_id)
    return await converter(result)


@api.post('/tradeOrder/post/')
async def post_tradeOrder(request,form:TradeOrderForm):
    """
    type = ["SELL","BUY"]\n
    code = ["NORMAL","COMPLETE","CANCELED"]\n
    모든 사용자가 asset을 소유중이라 가정.
    """
    form = form.dict()
    result = await make_trade_order(form)
    # await result.async_save()
    return await converter(result)

@database_sync_to_async
def make_trade_order(form)->TradeOrder:
    result = TradeOrder.custom_create(**form)
    return result


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
        
def fail_message(msg:str):
    return {'system':{
        "result": FAILED,
        "messages":msg
    }}
        
@sync_to_async
def aprint(msg):
    pprint(str(msg))
    

@database_sync_to_async
def get_product_by_name(product_name):
    return Product.objects.get(name=product_name)


@database_sync_to_async
def get_user_by_id(user_id):
    return User.objects.get(pk=user_id)

@database_sync_to_async
def get_type(type):
    return Type.objects.get(type=type)

@database_sync_to_async
def get_code(code):
    return Code.objects.get(code=code)

@database_sync_to_async
def model_save(model):
    model.save()
