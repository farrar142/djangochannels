from django.db import models
from commons.models import *
from commons.const import *
from accounts.models import *
from stocks.models import *
# Create your models here.
class Trade_Order(AsyncModel):    
    class Meta:
        db_table = "trade_order"
    trade_order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tradeorder')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='tradeorder')
    point = models.IntegerField('거래가격')
    code = models.ForeignKey(Code,on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type,on_delete=models.DO_NOTHING)
    fee = models.IntegerField('수수료',default=0)
    reg_date = models.DateTimeField('게시날짜', auto_now_add=True)
    update_date = models.DateTimeField('수정날짜', auto_now_add=True)
    
    def 자기자신을_업데이트하는_로직(self):
        result = self.asset_item.filter(trade_order_id = self.pk,code_id=MARKET)
        if not result.exists():
            self.code_id = 4
            self.save()
        ##need messaging
        result = Trade_Order.objects.prefetch_related('asset_item').filter(pk=self.pk).annotate(asset_item_code_id=models.F('asset_item__code__pk'),asset_amount=models.Count('asset_item__pk'))
        return result
 
        
        
class Trade_History(AsyncModel):
    class Meta:
        db_table = "trade_history"
    trade_history_id = models.AutoField(primary_key=True)
    trade_order = models.ForeignKey(Trade_Order,on_delete=models.CASCADE,related_name='Trade_History')
    code = models.ForeignKey(Code,on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type,on_delete=models.DO_NOTHING)
    point = models.IntegerField('거래가격')
    reg_date = models.DateTimeField('게시날짜', auto_now_add=True)
    
    

    