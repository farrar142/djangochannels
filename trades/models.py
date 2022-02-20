from django.db import models
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
                p_name,
                {
                    "type":"update",
                    "유형": 유형,
                    "거래량":총거래량,
                }
            )
        
        if self.cur_amount == 0:
            self.code_id = 4
            self.save()
        ##need messaging
        return self
 
        
        
class Trade_History(AsyncModel):
    class Meta:
        db_table = "trade_history"
    trade_history_id = models.AutoField(primary_key=True)
    trade_order = models.ForeignKey(Trade_Order,on_delete=models.CASCADE,related_name='Trade_History')
    code = models.ForeignKey(Code,on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type,on_delete=models.DO_NOTHING)
    point = models.IntegerField('거래가격')
    reg_date = models.DateTimeField('게시날짜', auto_now_add=True)
    
    

    