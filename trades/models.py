from django.db import connection
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from unidecode import unidecode
from commons.models import *
from commons.const import *
from accounts.models import *
from stocks.models import *
from mysite.functions import *
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
    reg_date = models.DateTimeField('게시날짜', auto_now_add=True)
    update_date = models.DateTimeField('수정날짜', auto_now_add=True)
    
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
        
    @timer
    def 자기자신을_업데이트하는_로직(self,type_id,총거래량):
        if type_id == 1:
            유형 = "매수"
        elif type_id == 2:
            유형 = "매도"
        if 총거래량 > 0:
            channel_layer = get_channel_layer()
            p_name = u'product_%s' % unidecode(self.product.name)
            async_to_sync(channel_layer.group_send)(
                u'%s'%unidecode('chat_Notify'),
                {
                    "type":"trade_result",
                    "유형": 유형,
                    "거래량":총거래량,
                }
            )
        
        if self.cur_amount == 0:
            self.code_id = 4
            self.save()
        ##need messaging
        return self
    @classmethod
    def get_oldest_order(cls,user_id,**kwrgs):
        return cls.objects.filter(**kwrgs).exclude(user_id=user_id).order_by('reg_date').first()
        
    
    @classmethod    
    def asset_item_updater(cls,target_to_id,my_to_id,type_id,amount):
        
        if type_id == BUY:
            cls.status_updater(my_to_id,target_to_id,amount)
        elif type_id == SELL:
            cls.status_updater(target_to_id,my_to_id,amount)
            
    @classmethod    
    def status_updater(cls,update_to_id,delete_order_id,amount):
        
        update = f"""
        update asset_item set code_id={HOLD} where trade_order_id = {update_to_id} and code_id={MARKET} limit {amount} 
        """

        delete = f"delete from asset_item where trade_order_id = {delete_order_id} and code_id = {MARKET} limit {amount}"

        with connection.cursor() as cursor:
            cursor.execute(update)
            cursor.execute(delete)
class Buyer(Trade_Order):
    class Meta:
        proxy = True        
        
    @classmethod
    def asset_item_bulk_creater(cls,user_id,product_id,trade_order_id,point,quantity):
        cur_time = timezone.now()
        cur_time_format = f"{cur_time:%Y-%m-%d %H:%M:%S}"
        target = [(user_id,product_id,trade_order_id,MARKET,BUY,point,cur_time_format)for i in range(0,quantity)]
        
        multiple_row_insert =f"""
        insert into asset_item 
        (user_id,product_id,trade_order_id,code_id,type_id,point,reg_date) values {value_parser(target)}
        """
        with connection.cursor() as cursor:
            cursor.execute(multiple_row_insert)
            
class Seller(Trade_Order):
    class Meta:
        proxy = True
            
    @classmethod
    def asset_item_bulk_updater(cls,trade_order_id,code_id,type_id,product_id,user_id,quantity,target=['code_id','type_id','trade_order_id']):
        
        update = f"""
        update asset_item set code_id={MARKET},type_id={SELL},trade_order_id={trade_order_id} where product_id = {product_id} and user_id={user_id} and code_id={HOLD} and type_id={BUY} limit {quantity} 
        """
        
        with connection.cursor() as cursor:
            cursor.execute(update)
        
class Trade_History(AsyncModel):
    class Meta:
        db_table = "trade_history"
    trade_history_id = models.AutoField(primary_key=True)
    trade_order = models.ForeignKey(Trade_Order,on_delete=models.CASCADE,related_name='Trade_History')
    code = models.ForeignKey(Code,on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type,on_delete=models.DO_NOTHING)
    point = models.IntegerField('거래가격')
    reg_date = models.DateTimeField('게시날짜', auto_now_add=True)
    
    

    