from typing import List
from django.http import HttpResponse, JsonResponse
from ninja import Router
from django.db.models import *
from django.core.cache import cache

from asgiref.sync import sync_to_async
from mysite.serializer import aconverter
from mysite.forms import *
from assets.models import Asset_Item

router = Router()
wallet_api = Router()

@sync_to_async
@router.get('/get')
def get_asset_items(request,user_id:int=0,product_id:int=0,type_id:int=0,code_id:int=0):
    
    cache_key = f"asset_items_{user_id}_{product_id}_{type_id}_{code_id}"
    result = cache.get(cache_key,None)
    if not result:
        result = Asset_Item.objects.values('product_id','user_id','type__type','code__code').annotate(amount=Count('pk'),asset_item_type=F('type__type'),asset_item_code=F('code__code'))
        if user_id:
            result = result.filter(user_id=user_id)
        if product_id:
            result = result.filter(product_id=product_id)
        if type_id:
            result = result.filter(type_id=type_id)
        if code_id:
            result = result.filter(code_id=code_id)
        cache.set(cache_key,result,60*60)
    return result
    # return await sync_to_async(HttpResponse)(result)
    # return await aconverter(result)

@sync_to_async
@router.post('/post')
def post_asset_item(request,form:Asset_ItemForm):
    """
    LEGACY
    test기능\n
    trade_order : null 로설정하면\n
    trade_order_id = null로 들어감.
    """
    kwargs = form.dict()
    kwargs.pop('token')
    kwargs.update(user=request.user)
    print(request.user)
    result:Asset_Item = Asset_Item(**kwargs)
    result.save()
    return result

@sync_to_async
@router.post('/post/bulk/{amount}')
def post_asset_item(request,amount:int,form:Asset_ItemForm):
    """
    LEGACY
    test기능\n
    """
    result = Asset_Item.async_bulk_post(amount,**form.dict())
    return result