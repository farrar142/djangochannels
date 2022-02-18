from commons.models import *
from mysite.const import *
from accounts.models import *
from assets.models import *


def transaction(*args,**kwargs):
    ##parameter init
    t_dict = kwargs.copy()
    t_dict.pop('point')
    t_dict.pop('quantity')
    t_dict.pop('fake_token')
    t_dict.update(code_id=1)
    quantity:int = kwargs['quantity']
    point:int = kwargs['point']
    type_id:int = kwargs['type_id']
    asset_id:int = kwargs['asset_id']
    fake_token:str = kwargs['fake_token']
    
    ##Trade_Order 생성
    trade_order = Trade_Order(**t_dict)
    trade_order.save()
    
    """
    sell쪽에선 asset item 업데이트.
    /////
    """
    #quantity,
    if type_id == SELL:
        #asset_item 가져옴
        my_trades_list = Asset_Item.objects.filter(asset_id=asset_id,trade_order=trade_order,asset__user__username=fake_token,code_id=HOLD,type_id=BUY)[:quantity]
        
        #asset_item 수량체크 db hit 1
        if my_trades_list.count() < quantity:
            return fail_message("판매자 asset item 보유수량 부족")
        
        #업데이트
        for asset_item in my_trades_list:
            asset_item.code_id = MARKET
            asset_item.type_id = SELL
            
        Asset_Item.objects.bulk_update(my_trades_list,['code_id','type_id'])
        
    #매도/매수시 동일하게 Trade_History를 생성    
    elif type_id == BUY:
        ## 자산 관련 validate  필요
        user = Point.objects.get(user__username=fake_token)
        
        #asset_item 생성함
        my_trades_list = Asset_Item.objects.bulk_create(##db hit 1
            [Asset_Item(asset_id=asset_id,trade_order=trade_order,code_id=MARKET,type_id=BUY,point=point) for i in range(0,quantity) ]
        )#filter나all()은 queryset을 반환하지만 이놈은 Trade_History이 담긴 List를반환
        
    #만들어진 list와 db모델의 id를 동기화 시키기위해 id만 추출해옴
    my_ids = [i.pk for i in my_trades_list]
    
    #거래 로직
    if type_id==BUY:
        #셀러리로 돌릴예정
        transaction_logic(BUY,asset_id,point,quantity,my_ids)
    elif type_id==SELL:
        transaction_logic(SELL,asset_id,point,quantity,my_ids)
        
    """
    buy쪽엔 insert asset_item
    sell쪽엔 delete asset_item
    """
    return trade_order

def transaction_logic(type_id,asset_id,point,quantity,my_ids):
    #마켓의 상품을 quantity만큼 가져와서 count를함.
    if type_id == BUY:
        #구매인 경우 상대방의 SELL type을 가져와서 개수를 셈.
        targets = Asset_Item.objects.filter(
                code_id=MARKET,type_id=type_id,point=point,                
                ).order_by('reg_date')[:quantity]
        count = targets.count()
        
    #장고orm에서업데이트
        for i in targets:
            i.code_id = HOLD
        
    #code_id를 db에 업데이트함과 동시에 update가 이뤄진 개수를 리턴받음
    #자기가 가진 id중에서 업데이트가 이루어진 target갯수만큼을 가져옴
"""
if 매수시.
    TradeOrder 생성
    AssetItem 생성 CODE = MARKET , TYPE = BUY
    거래로직()


elif 매도시.
    TradeOrder생성
    Asset_Item 업데이트 CODE = HOLD->MARKET , TYPE = BUY->SELL

거래로직()

def 거래로직():
    1.등록한 상품들과 등록된 상품들을 비교.












"""