from ninja import Router
from django.db.models import *

from mysite.serializer import converter
from mysite.forms import *
from mysite.api import *
from .models import *
from trades.logics import transaction
router = Router()

@router.get('/get')

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
    result=result.order_by('reg_date')
    return await converter(result)


@router.post('/post/')
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
