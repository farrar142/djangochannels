from django.db import models
from commons.models import *
from mysite.const import *
from accounts.models import *
# Create your models here.
class Trade_Order(AsyncModel):    
    class Meta:
        db_table = "trade_order"
    trade_order_id = models.AutoField(primary_key=True)
    asset = models.ForeignKey(Asset,on_delete=models.CASCADE,related_name='tradeorder')
    code = models.ForeignKey(Code,on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type,on_delete=models.DO_NOTHING)
    fee = models.IntegerField('수수료',default=0)
    reg_date = models.DateTimeField('게시날짜', auto_now_add=True)
    update_date = models.DateTimeField('수정날짜', auto_now_add=True)
 
        
        
class Trade_History(AsyncModel):
    class Meta:
        db_table = "trade_history"
    trade_history_id = models.AutoField(primary_key=True)
    trade_order = models.ForeignKey(Trade_Order,on_delete=models.CASCADE,related_name='Trade_History')
    code = models.ForeignKey(Code,on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type,on_delete=models.DO_NOTHING)
    point = models.IntegerField('거래가격')
    reg_date = models.DateTimeField('게시날짜', auto_now_add=True)
    
    

    