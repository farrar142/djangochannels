from ninja import NinjaAPI,Form,Schema
from django.db.models import *
from channels.db import database_sync_to_async
from pprint import pprint

from mysite.serializer import converter
from commons.const import *
from stocks.models import *
from trades.models import Trade_Order,Trade_History 
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
##all(),get() == lazy loading
##get() == eager loading
class ProductForm(Schema):
    name : str
    category_id : int
    
class Trade_OrderForm(Schema):
    user_id : int
    product_id : int
    point : int
    quantity : int
    type_id : int
    fake_token : str = "admin"
    
class Asset_ItemForm(Schema):
    user_id : int
    product_id : int
    point : int
    code_id : int
    type_id : int
    trade_order : Trade_OrderForm = None
    

@api.get('/products')
async def get_product_all(request):
    result = Product.objects.all().annotate(category_name=F('category_id__name'))#db에 query하지않음
    return await converter(result)

@api.get('/product/get/{product_id}')
async def get_product(request,product_id:int):
    result = Product.objects.filter(**{"pk":product_id}).annotate(category_name=F('category_id__name'))
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

@api.get('/asset/items/get')
async def get_asset_items(request,user_id:int=0,product_id:int=0,type_id:int=0,code_id:int=0):
    result = Asset_Item.objects.all().annotate(amount=Count('pk'),asset_item_type=F('type__type'),asset_item_code=F('code__code'))
    if user_id:
        result = result.filter(user_id=user_id)
    if product_id:
        result = result.filter(product_id=product_id)
    if type_id:
        result = result.filter(type_id=type_id)
    if code_id:
        result = result.filter(code_id=code_id)
    
    return await converter(result)

@api.post('/asset/item/post')
async def post_asset_item(request,form:Asset_ItemForm):
    """
    test기능\n
    trade_order : null 로설정하면\n
    trade_order_id = null로 들어감.
    """
    result:Asset_Item = Asset_Item(**form.dict())
    await result.async_save()
    return await converter(result)

@api.post('/asset/item/post/bulk/{amount}')
async def post_asset_item(request,amount:int,form:Asset_ItemForm):
    """
    test기능\n
    """
    result = await Asset_Item.async_bulk_post(amount,**form.dict())
    return await converter(result)

@api.get('/trade_orders')
async def get_trade_order(
    request,product_id:int=0,
    user_id:int=0,type_id=0,code_id=0,asset_item_code_id:int=0
    ):
    """
    ?user_id=   1 -> 1번유저의 거래기록 반환
    
    ?product_id 1 -> 1번프로덕트의 거래기록 반환
    
    ?type_id=   1 -> BUY기록
                2 -> SELL기록
    
    ?code_id=   1 -> NORMAL기록
                2 -> COMPLETE기록
                3 -> CANCELED기록
                
    ?asset_item_code_id=   1 -> Trade_Order의 NORMAL기록
                2 -> Trade_Order의 COMPLETE기록
                3 -> Trade_Order의 CANCELED기록
    
    """
    result = Trade_Order.objects.prefetch_related('asset_item').annotate(
        user_name=F('user__username'),
        product_name=F('product__name'),
        type_name=F('type__type'),
        trade_amount=Count('asset_item'),
        price=F('asset_item__point'),
        asset_item_code_id=F('asset_item__code__pk')
    )
    #await aprint(result.query)
    #return await converter(result)
    ##Trade_History의 상태를 판별해서 카운트해야됨.
    if product_id >= 1:
        result = result.filter(product_id=product_id)
    if user_id >= 1:
        result = result.filter(user_id=user_id)
    if type_id >= 1:
        result = result.filter(type_id=type_id)
    if code_id >= 1:
        result = result.filter(code_id=code_id)
    if asset_item_code_id >= 1:
        result = result.filter(asset_item__code_id=asset_item_code_id)
    return await converter(result)


@api.post('/trade_Order/post/')
async def post_trade_order(request,form:Trade_OrderForm):
    """
    type = ["BUY","SELL"]\n
    code = ["NORMAL","COMPLETE","CANCELED"]\n
    모든 사용자가 asset을 소유중이라 가정.
    """
    form = form.dict()
    result = await make_trade_order(form)
    # await result.async_save()
    return await converter(result)

@database_sync_to_async
def make_trade_order(form):
    result = transaction(**form)
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