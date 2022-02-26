from commons.models import *
from commons.const import *
from accounts.models import *
from assets.models import *
from django.db.models import QuerySet
from mysite.functions import *
from trades.tasks import *

@timer
def transaction(*args,**kwargs):
    ##parameter init
    t_dict = kwargs.copy()
    #t_dict.pop('point')
    tmp_amount = t_dict.pop('amount')
    t_dict.pop('fake_token')
    t_dict.update(code_id=5)
    t_dict.update(reg_amount=tmp_amount)
    t_dict.update(cur_amount=tmp_amount)
    quantity:int = kwargs['amount']
    point:int = kwargs['point']
    type_id:int = kwargs['type_id']
    product_id:int = kwargs['product_id']
    fake_token:str = kwargs['fake_token']
    user = User.objects.get(username=fake_token)
    ##Trade_Order 생성
    trade_order = Trade_Order(**t_dict)
    trade_order.user = user
    
    wallet = Wallet.objects.get_or_create(user=user,product_id=product_id)[0]
    """
    sell쪽에선 asset item 업데이트.
    /////
    """
    #quantity,
    if type_id == SELL:
        #asset_item 가져옴
        wallet_updater.delay(wallet.pk,-quantity)
        
        if wallet.amount < quantity:
            return fail_message("판매자 asset item 보유수량 부족")
         
    elif type_id == BUY:
        points = Point.objects.get(user_id=user.pk)
        ## 자산 관련 validate  필요
        if False:
            return
        
    trade_order.save()
        
    if type_id == SELL:
        selling_items.delay(trade_order.pk,MARKET,SELL,product_id,user.pk,quantity,['code_id','type_id','trade_order_id'])
    elif type_id == BUY:
        #asset_item 생성함
        buying_items.delay(user.pk,product_id,trade_order.pk,point,quantity)
        
        #filter나all()은 queryset을 반환하지만 이놈은 Trade_History이 담긴 List를반환
    return trade_logic(trade_order,product_id,user,wallet,type_id,quantity,point,0)

@timer   
def trade_logic(
    my_trade_order:Trade_Order,product_id,user:User,wallet,
    type_id,amount,point,총거래량):
    
    if type_id == BUY:
        target_type_id = SELL
    else:
        target_type_id = BUY
    #X프로덕트의 가장 오래된 Y트레이드오더 중에 처음껄 가져옴. db hit 1                
    target_trade_order:QuerySet = Trade_Order.get_oldest_order(
        user.pk,
        product_id=product_id,point=point,type_id=target_type_id,code_id=MARKET,cur_amount__gte=1
        )
    if not target_trade_order:      
    #없다면 로직 종료
        return my_trade_order.자기자신을_업데이트하는_로직(type_id,0)
    
    #trade_order 업데이트
    
    #Y트레이드 오더의 cur_amount 가 거래량보다 많다면
    if target_trade_order.cur_amount >= amount:
        target_trade_order.cur_amount -= amount
        거래된량 = amount
        남은거래량 = 0
    #y트레이드 오더의 cur_amount가 거래량보다 적다면
    else:
        거래된량 = target_trade_order.cur_amount
        남은거래량 = amount - 거래된량
        target_trade_order.cur_amount = 0
    my_trade_order.cur_amount -= 거래된량
    if type_id == BUY:
        wallet_updater.delay(wallet.pk,거래된량)
    
    my_trade_order.save()
    target_trade_order.save()
    target_trade_order.자기자신을_업데이트하는_로직(target_type_id,거래된량)
    asset_item_updater.delay(target_trade_order.pk,my_trade_order.pk,type_id,거래된량)
    
    if 남은거래량 > 0:
        return trade_logic(my_trade_order,product_id,user,wallet,type_id,남은거래량,point,총거래량+거래된량)
    else:
        return my_trade_order.자기자신을_업데이트하는_로직(type_id,총거래량+거래된량)
        
    
        