from commons.models import *
from commons.const import *
from accounts.models import *
from assets.models import *


def transaction(*args,**kwargs):
    ##parameter init
    t_dict = kwargs.copy()
    #t_dict.pop('point')
    t_dict.pop('quantity')
    t_dict.pop('fake_token')
    t_dict.update(code_id=5)
    quantity:int = kwargs['quantity']
    point:int = kwargs['point']
    type_id:int = kwargs['type_id']
    product_id:int = kwargs['product_id']
    fake_token:str = kwargs['fake_token']
    user = User.objects.get(username=fake_token)
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
        my_trades_list = Asset_Item.objects.filter(product_id=product_id,user_id=user.pk,code_id=HOLD,type_id=BUY)[:quantity]
        
        #asset_item 수량체크 db hit 1
        if my_trades_list.count() < quantity:
            return fail_message("판매자 asset item 보유수량 부족")
        
        #업데이트
        for asset_item in my_trades_list:
            asset_item.code_id = MARKET
            asset_item.type_id = SELL
            asset_item.trade_order_id = trade_order.pk
            
        Asset_Item.objects.bulk_update(my_trades_list,['code_id','type_id','trade_order_id'])
        
    #매도/매수시 동일하게 Trade_History를 생성    
    elif type_id == BUY:
        ## 자산 관련 validate  필요
        points = Point.objects.get(user_id=user.pk)
        
        #asset_item 생성함
        my_trades_list = Asset_Item.objects.bulk_create(##db hit 1
            [Asset_Item(user_id=user.pk,product_id=product_id,trade_order=trade_order,code_id=MARKET,type_id=BUY,point=point) for i in range(0,quantity) ]
        )#filter나all()은 queryset을 반환하지만 이놈은 Trade_History이 담긴 List를반환
    return trade_logic(trade_order,product_id,user,type_id,quantity,point)
        
def trade_logic(
    trade_order:Trade_Order,product_id,user:User,
    type_id,amount,point):
    
    if type_id == BUY:
        
        #X프로덕트의 가장 오래된 Y트레이드오더 중에 처음껄 가져옴. db hit 1
                
        target_trade_order:Trade_Order = Trade_Order.objects.filter(
            product_id=product_id,point=point,type_id=SELL,code_id=MARKET
            ).exclude(user_id=user.pk).order_by('reg_date').first()
        if not target_trade_order:      
        #없다면 로직 종료
            return trade_order.자기자신을_업데이트하는_로직()
        #Y트레이드 오더중에 MARKET에 올라와있고 SELL인 녀석들을 amount만큼 필터
        target_asset_items = Asset_Item.objects.filter(
            trade_order = target_trade_order,type_id=SELL,code_id = MARKET
            )[:amount]
        
        #limit이나 offset객체엔 .delete()사용불가...
        target_asset_items = [i.pk for i in target_asset_items]
        target_asset_items = Asset_Item.objects.filter(pk__in=target_asset_items)
        
        #Y트레이드 오더의 Asset_Item들을 Delete : db hit 2
        거래된량 = target_asset_items.count()
        target_asset_items.delete()
        
        #거래된량만큼 내 AssetItem들을 업데이트 : db hit 3
        #리스트 인덱스 over되어도 오류나지 않고 정상반환함.
        my_asset_items = Asset_Item.objects.filter(
            trade_order = trade_order,type_id = BUY,code_id = MARKET
        )[:거래된량]
        for item in my_asset_items:
            item.code_id = HOLD
        
        Asset_Item.objects.bulk_update(my_asset_items,['code_id'])
        
        #상대방의 거래를 갱신하고 상대방에게 알림을 할 에정
        target_trade_order.자기자신을_업데이트하는_로직()
        
        #아직 처리해야 될 거래가 남아있다면 재귀호출. 없다면 return
        left = amount - 거래된량
        if left >= 1:
            return trade_logic(
                trade_order,product_id,user,type_id,left,point
            )
        else:
            return trade_order.자기자신을_업데이트하는_로직()
        
        