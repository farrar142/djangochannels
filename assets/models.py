from django.db import models
from accounts.models import User
from trades.models import Trade_Order
from commons.models import *
from stocks.models import Product
# Create your models here.
#
#
    
class Asset_Item(AsyncModel):
    class Meta:
        db_table = "asset_item"
    asset_item_id = models.AutoField(primary_key=True)
    point = models.IntegerField(null=True,blank=True)
    reg_date = models.DateTimeField('게시날짜', auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="asset_item")
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    code = models.ForeignKey(Code,on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type,on_delete=models.DO_NOTHING)
    trade_order = models.ForeignKey(Trade_Order,on_delete=models.DO_NOTHING,null=True,related_name="asset_item")