from ninja import Router
from django.db.models import *

from mysite.serializer import converter
from mysite.forms import *
from assets.models import Asset_Item

router = Router()
wallet_api = Router()


@router.get('/get')
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

@router.post('/post')
async def post_asset_item(request,form:Asset_ItemForm):
    """
    test기능\n
    trade_order : null 로설정하면\n
    trade_order_id = null로 들어감.
    """
    kwargs = form.dict()
    kwargs.pop('token')
    kwargs.update(user=request.user)
    print(request.user)
    result:Asset_Item = Asset_Item(**kwargs)
    await result.async_save()
    return await converter(result)

@router.post('/post/bulk/{amount}')
async def post_asset_item(request,amount:int,form:Asset_ItemForm):
    """
    test기능\n
    """
    result = await Asset_Item.async_bulk_post(amount,**form.dict())
    return await converter(result)