from django.db import models
from accounts.models import *
from trades.models import *
from commons.models import *
# Create your models here.
#
#
    
class Asset_Item(AsyncModel):
    class Meta:
        db_table = "asset_item"
    asset_item_id = models.AutoField(primary_key=True)
    point = models.IntegerField(null=True,blank=True)
    reg_date = models.DateTimeField('게시날짜', auto_now_add=True)
    asset = models.ForeignKey(Asset,on_delete=models.CASCADE,related_name="asset_item")
    code = models.ForeignKey(Code,on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type,on_delete=models.DO_NOTHING)
    trade_order = models.ForeignKey(Trade_Order,on_delete=models.DO_NOTHING,null=True)