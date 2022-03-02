from django.db import connection
from django.utils import timezone
from django.apps import apps
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync,sync_to_async
from unidecode import unidecode
from commons.models import *
from commons.const import *
from accounts.models import *
from stocks.models import *
from mysite.functions import *
from trades.tasks import *
# Create your models here.
class Trade_Order(AsyncModel):    
    class Meta:
        db_table = "trade_order"
    trade_order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tradeorder')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='tradeorder')
    point = models.IntegerField('거래가격')
    reg_amount = models.IntegerField('등록수량')
    cur_amount = models.IntegerField('현재수량')
    code = models.ForeignKey(Code,on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type,on_delete=models.DO_NOTHING)
    fee = models.IntegerField('수수료',default=0)
    
    @classmethod
    def factory(cls,user_id,product_id,point,amount,type_id,code_id=MARKET,cur_amount=False):
        """
        this function doesn't valid User's assetItem .just create and
        update AssetItem
        """
        cls.inherit_check()
        result = cls()
        result.user_id = user_id
        result.product_id = product_id
        result.point = point
        result.reg_amount = amount
        if cur_amount == 0:
            result.cur_amount = cur_amount
        else:
            result.cur_amount = amount
        print(result.cur_amount)
        result.code_id = code_id
        result.type_id = type_id
        return result
    
    def call_task(self):
        set_items.delay(self.__class__.__name__,self.pk)
        
    
    def set_assets(self):
        raise Exception("UnImplemented")
    def transaction_succeed(self):
        raise Exception("UnImplemented")
    @classmethod
    def inherit_check(cls):        
        if issubclass(Trade_Order,cls):
            raise Exception('you cannot call this from parent')
    @sync_to_async
    def acancel(self):
        return self.cancel()
    
    def cancel(self):
        if self.type_id == SELL:
            query = f"""
            update asset_item set code_id={HOLD},type_id={BUY},trade_order_id={self.pk} where product_id = {self.product_id} and user_id={self.user_id} and code_id={MARKET} and type_id={SELL} 
            """
            with connection.cursor() as cursor:
                cursor.execute(query)
        
        self.code_id = CANCELED
        self.save()
        return self
    
    def gen_datas(self):
        cur_time = timezone.now()
        cur_time_format = f"{cur_time:%Y-%m-%d %H:%M:%S}"
        target = [(self.user.pk,self.product.pk,self.pk,self.code.pk,self.type.pk,self.point,cur_time_format)for i in range(0,self.reg_amount)]
        
            
        multiple_row_insert =f"""
        insert into asset_item 
        (user_id,product_id,trade_order_id,code_id,type_id,point,reg_date) values {value_parser(target)}
        """    
        
        with connection.cursor() as cursor:
            cursor.execute(multiple_row_insert)
        
    def 자기자신을_업데이트하는_로직(self,type_id,총거래량):
        if type_id == 1:
            유형 = "매수"
        elif type_id == 2:
            유형 = "매도"
        print(f"총거래량 : {총거래량}")
        if 총거래량 > 0:
            channel_layer = get_channel_layer()
            p_name = u'product_%s' % unidecode(self.product.name)
            async_to_sync(channel_layer.group_send)(
                u'%s'%unidecode('chat_Notify'),
                {
                    "type":"send_all_trade_order",
                    "마켓": self.product.name,
                    "유형": 유형,
                    "거래량":총거래량,
                }
            )
        
        if self.cur_amount == 0:
            self.code_id = 4
        self.save()
        ##need messaging
        return self
    def get_oldest_order(self):
        target_type_id = SELL if self.type_id == BUY else BUY
        model = "Seller" if self.type_id == BUY else "Buyer"
        result = apps.get_model('trades',model).objects.filter(
            product_id=self.product_id,point=self.point,
            type_id=target_type_id,code_id=MARKET,cur_amount__gte=1
            ).exclude(user_id=self.user_id).order_by('reg_date')
        return result.first()
    
class Buyer(Trade_Order):
    class Meta:
        proxy = True        
        
    def set_assets(self):
        cur_time = timezone.now()
        cur_time_format = f"{cur_time:%Y-%m-%d %H:%M:%S}"
        target = [(self.user_id,self.product_id,self.trade_order_id,self.code_id,BUY,self.point,cur_time_format)for i in range(0,self.reg_amount)]
        
        multiple_row_insert =f"""
        insert into asset_item 
        (user_id,product_id,trade_order_id,code_id,type_id,point,reg_date) values {value_parser(target)}
        """
        with connection.cursor() as cursor:
            cursor.execute(multiple_row_insert)
            
    def transaction_succeed(self,amount):
        query = f"""
        update asset_item set code_id={HOLD} where trade_order_id = {self.pk} and code_id={MARKET} limit {amount} 
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
        
            
class Seller(Trade_Order):
    class Meta:
        proxy = True
        
    
    def set_assets(self,target=['code_id','type_id','trade_order_id']):
        
        update = f"""
        update asset_item set code_id={self.code_id},type_id={SELL},trade_order_id={self.pk} where product_id = {self.product_id} and user_id={self.user_id} and code_id={HOLD} and type_id={BUY} limit {self.reg_amount} 
        """
        
        with connection.cursor() as cursor:
            cursor.execute(update)
    def transaction_succeed(self,amount):
        
        query = f"delete from asset_item where trade_order_id = {self.pk} and code_id = {MARKET} limit {amount}"

        with connection.cursor() as cursor:
            cursor.execute(query)
        
class Trade_History(AsyncModel):
    class Meta:
        db_table = "trade_history"
    trade_history_id = models.AutoField(primary_key=True)
    trade_order = models.ForeignKey(Trade_Order,on_delete=models.CASCADE,related_name='Trade_History')
    code = models.ForeignKey(Code,on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type,on_delete=models.DO_NOTHING)
    point = models.IntegerField('거래가격')
    reg_date = models.DateTimeField('게시날짜', auto_now_add=True)
    
    

    