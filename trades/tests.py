import time
from django.test import TestCase
from mysite.datas import gen_datas
from accounts.models import User, Wallet
from trades.models import *
from trades.tasks import *
from pprint import pprint
IAM = 1
MY_PRODUCT = 1
TARGET = 2 
TARGET_PRODUCT = 2

def making_trade_order(user,product_id,point,reg_amount,cur_amount,type_id):
    """
    Main TRADING API
    """
    print("trade order entered")
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
    trade_order.set_assets() 
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
        return trade_order_updater(my_trade_order.pk,type_id,0)
    
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
    trade_order_updater(target_trade_order.pk,target_type_id,거래된량)
    if my_trade_order.type_id == BUY:
        asset_item_updater(my_trade_order.pk,target_trade_order.pk,type_id,거래된량)
    else:
        asset_item_updater(target_trade_order.pk,my_trade_order.pk,type_id,거래된량)
        
    
    if 남은거래량 > 0:
        return transaction_logic(my_trade_order,product_id,wallet,type_id,남은거래량,point,총거래량+거래된량)
    else:
        return trade_order_updater(my_trade_order.pk,type_id,총거래량+거래된량)
        
    
        
class TransactionTest(TestCase):
    #
    @classmethod
    def setUpTestData(cls):
        gen_datas()
        
    def test_gen_datas_test(self):
        user = User.objects.get(pk=IAM)
        wallet = Wallet.objects.get(pk=user.pk)
        trade_order = Trade_Order.objects.filter(user_id=1,product_id=1)
        b=wallet.my_selling_stocks(1)['amount']
        c=wallet.my_holding_stocks(1)['amount']
        
    def test_A유저가_50포인트만큼_500개를_팜_B_유저가_50포인트만큼_500개를_삼(self):
        iam = Wallet.objects.get(pk=IAM)
        making_trade_order(iam,MY_PRODUCT,50,500,500,SELL)
        target = Wallet.objects.get(pk=TARGET)
        making_trade_order(target,MY_PRODUCT,50,500,500,BUY)
        a = iam.my_selling_stocks(IAM)
        b = iam.my_holding_stocks(IAM)
        c = target.my_selling_stocks(MY_PRODUCT)
        d = target.my_holding_stocks(MY_PRODUCT)
        self.assertEquals(a['amount'],0)
        self.assertEquals(b['amount'],4500)
        self.assertEquals(c['amount'],0)
        self.assertEquals(d['amount'],5500)
        
    def test_A유저가_50포인트만큼_500개를_팜_B_유저가_50포인트만큼_250개를_삼_A유저는_250개가_남아야됨(self):
        iam = Wallet.objects.get(pk=IAM)
        making_trade_order(iam,MY_PRODUCT,50,500,500,SELL)
        target = Wallet.objects.get(pk=TARGET)
        making_trade_order(target,MY_PRODUCT,50,250,250,BUY)
        a = iam.my_selling_stocks(IAM)
        b = iam.my_holding_stocks(IAM)
        c = target.my_selling_stocks(MY_PRODUCT)
        d = target.my_holding_stocks(MY_PRODUCT)
        self.assertEquals(a['amount'],250)
        self.assertEquals(b['amount'],4500)
        self.assertEquals(c['amount'],0)
        self.assertEquals(d['amount'],5250)
        
        
    def test_A유저가_50포인트만큼_500개를_삼_B_유저가_50포인트만큼_250개를_팜_A유저는_250개가_남아야됨(self):
        iam = Wallet.objects.get(pk=IAM)
        making_trade_order(iam,MY_PRODUCT,50,500,500,BUY)
        target = Wallet.objects.get(pk=TARGET)
        making_trade_order(target,MY_PRODUCT,50,250,250,SELL)
        a = iam.my_selling_stocks(IAM)
        b = iam.my_holding_stocks(IAM)
        c = target.my_selling_stocks(MY_PRODUCT)
        d = target.my_holding_stocks(MY_PRODUCT)
        self.assertEquals(a['amount'],0)
        self.assertEquals(b['amount'],5250)
        self.assertEquals(c['amount'],0)
        self.assertEquals(d['amount'],4750)
        
    def test_위의_상황에서_A유저가_거래를_취소함_그리고_B유저가_또50포인트만큼_250개를팜(self):
        iam = Wallet.objects.get(pk=IAM)
        making_trade_order(iam,MY_PRODUCT,50,500,500,BUY)
        target = Wallet.objects.get(pk=TARGET)
        making_trade_order(target,MY_PRODUCT,50,250,250,SELL)
        my_order =iam.tradeorder.all().last()
        print(my_order.product.name,my_order.cur_amount)
        my_order.cancel()
        making_trade_order(target,MY_PRODUCT,50,250,250,SELL)
        print(my_order.product.name,my_order.cur_amount,my_order.code.code)
        a = iam.my_selling_stocks(IAM)
        b = iam.my_holding_stocks(IAM)
        c = target.my_selling_stocks(MY_PRODUCT)
        d = target.my_holding_stocks(MY_PRODUCT)
        self.assertEquals(a['amount'],0)
        self.assertEquals(b['amount'],5250)
        self.assertEquals(c['amount'],250)
        self.assertEquals(d['amount'],4500)
        
    def test_위의_상황에서_A유저가_거래를_취소함_그리고_B유저가_또50포인트만큼_250개를삼(self):
        iam = Wallet.objects.get(pk=IAM)
        making_trade_order(iam,MY_PRODUCT,50,500,500,SELL)
        target = Wallet.objects.get(pk=TARGET)
        making_trade_order(target,MY_PRODUCT,50,250,250,BUY)
        my_order =iam.tradeorder.all().last()
        print(my_order.product.name,my_order.cur_amount)
        my_order.cancel()
        making_trade_order(target,MY_PRODUCT,50,250,250,BUY)
        print(my_order.product.name,my_order.cur_amount,my_order.code.code)
        a = iam.my_selling_stocks(IAM)
        b = iam.my_holding_stocks(IAM)
        c = target.my_selling_stocks(MY_PRODUCT)
        d = target.my_holding_stocks(MY_PRODUCT)
        self.assertEquals(a['amount'],0)
        self.assertEquals(b['amount'],4750)
        self.assertEquals(c['amount'],0)
        self.assertEquals(d['amount'],5250)
        
        
    def test_a의_amount는_0이_되고_b의_amount는_4750이_되어야함_캔슬기능_구현(self):
        iam = Wallet.objects.get(pk=IAM)
        making_trade_order(iam,MY_PRODUCT,50,500,500,SELL)
        target = Wallet.objects.get(pk=TARGET)
        making_trade_order(target,MY_PRODUCT,50,250,250,BUY)
        my_order =iam.tradeorder.all().last()
        print(my_order.product.name,my_order.cur_amount)
        my_order.cancel()
        making_trade_order(target,MY_PRODUCT,50,250,250,BUY)
        print(my_order.product.name,my_order.cur_amount,my_order.code.code)
        a = iam.my_selling_stocks(IAM)
        b = iam.my_holding_stocks(IAM)
        c = target.my_selling_stocks(MY_PRODUCT)
        d = target.my_holding_stocks(MY_PRODUCT)
        self.assertEquals(a['amount'],0)
        self.assertEquals(b['amount'],4750)
        self.assertEquals(c['amount'],0)
        self.assertEquals(d['amount'],5250)