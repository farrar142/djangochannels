from django.db import models
from django.db.models import *
from accounts.models import User
from trades.models import Trade_Order
from commons.models import *
from stocks.models import Product

from commons.const import *
# Create your models here.
#
#
    
class Asset_Item(AsyncModel):
    class Meta:
        db_table = "asset_item"
    asset_item_id = models.AutoField(primary_key=True)
    point = models.IntegerField(null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="asset_item")
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    code = models.ForeignKey(Code,on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type,on_delete=models.DO_NOTHING)
    trade_order = models.ForeignKey(Trade_Order,on_delete=models.DO_NOTHING,null=True,related_name="asset_item")
    
# class Wallet(AsyncModel):
#     class Meta:
#         db_table = "wallet"
        
#     user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="wallet")
#     product = models.ForeignKey(Product,on_delete=models.DO_NOTHING,related_name="wallet")
#     amount = models.IntegerField('보유량',default=0,null=True,blank=True)
    
#     def get_assets(self):
#         return Asset_Item.objects.filter(user=self.user,product=self.product,type_id=BUY,code_id=MARKET).count()