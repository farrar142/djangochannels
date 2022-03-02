from commons.models import *
from commons.const import *
from accounts.models import User,Wallet
from django.db.models import QuerySet
from mysite.functions import *
from trades.tasks import *
from trades.models import *
from custommiddle.models import Token

@timer
def trade_order_from_api(request,*args,**kwargs):
    ##parameter init
    quantity:int = kwargs['amount']
    point:int = kwargs['point']
    type_id:int = kwargs['type_id']
    product_id:int = kwargs['product_id']
    user = request.user
    ##Trade_Order 생성
    return making_trade_order(user,product_id,point,quantity,quantity,type_id)

def making_trade_order(user,product_id,point,reg_amount,cur_amount,type_id):
    """
    Main TRADING API
    """
    if type_id == SELL:
        trade_order = Seller.factory(user.pk,product_id,point,cur_amount,type_id,cur_amount=cur_amount)
    elif type_id == BUY:
        trade_order = Buyer.factory(user.pk,product_id,point,cur_amount,type_id,cur_amount=cur_amount)
    else:
        raise Exception('nope')
    
    wallet:Wallet = Wallet.objects.get(pk=user.pk)

    if type_id == SELL:
        
        if wallet.my_holding_stocks(product_id)['amount'] < reg_amount:
            return fail_message("판매자 asset item 보유수량 부족")

    elif type_id == BUY:
        points = Point.objects.get(user_id=user.pk)
        ## 자산 관련 validate  필요
        if False:
            return
        
    trade_order.save()       
    trade_order.call_task() 
    # if type_id == SELL:
    #     set_items.delay("Seller",trade_order.pk)
        
    # elif type_id == BUY:
    #     set_items.delay("Buyer",trade_order.pk)
        
    return transaction_logic(trade_order,product_id,wallet,type_id,reg_amount,point,0)

@timer   
def transaction_logic(
    my_trade_order:Trade_Order,product_id,wallet,
    type_id,amount,point,총거래량):
    
    if type_id == BUY:
        target_type_id = SELL
    else:
        target_type_id = BUY
    #X프로덕트의 가장 오래된 Y트레이드오더 중에 처음껄 가져옴. db hit 1           
    target_trade_order = my_trade_order.get_oldest_order()
    if not target_trade_order:      
    #없다면 로직 종료
        return trade_order_updater.delay(my_trade_order.pk,type_id,0).get()
    
    #trade_order 업데이트
    
    #Y트레이드 오더의 cur_amount 가 거래량보다 많다면
    if target_trade_order.cur_amount >= amount:
        target_trade_order.cur_amount -= amount
        거래된량,남은거래량 = amount,0
    #y트레이드 오더의 cur_amount가 거래량보다 적다면
    else:
        거래된량 = target_trade_order.cur_amount
        남은거래량 = amount - 거래된량
        target_trade_order.cur_amount = 0
        
    my_trade_order.cur_amount -= 거래된량
    
    my_trade_order.save()
    target_trade_order.save()
    trade_order_updater.delay(target_trade_order.pk,target_type_id,거래된량)
    if my_trade_order.type_id == BUY:
        asset_item_updater.delay(my_trade_order.pk,target_trade_order.pk,type_id,거래된량)
    else:
        asset_item_updater.delay(target_trade_order.pk,my_trade_order.pk,type_id,거래된량)
        
    
    if 남은거래량 > 0:
        return transaction_logic(my_trade_order,product_id,wallet,type_id,남은거래량,point,총거래량+거래된량)
    else:
        return trade_order_updater.delay(my_trade_order.pk,type_id,총거래량+거래된량).get()
        
    