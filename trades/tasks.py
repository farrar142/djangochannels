from __future__ import absolute_import
from datetime import datetime

from celery import shared_task
from django.db import connection
from commons.const import *
from trades.models import *
from assets.models import *
from mysite.functions import *


@shared_task
def selling_items(trade_order_id,code_id,type_id,product_id,user_id,quantity,target=['code_id','type_id','trade_order_id']):
    Seller.asset_item_bulk_updater(trade_order_id,code_id,type_id,product_id,user_id,quantity,target)    

    
@shared_task
def buying_items(user_id,product_id,trade_order_id,point,quantity):
    Buyer.asset_item_bulk_creater(user_id,product_id,trade_order_id,point,quantity)

@shared_task
def asset_item_updater(target_to_id,my_to_id,type_id,amount):
    Trade_Order.asset_item_updater(target_to_id,my_to_id,type_id,amount)
        
@shared_task
def wallet_updater(wallet_id,amount):
    wallet = Wallet.objects.get(pk=wallet_id)
    wallet.amount += amount
    wallet.save()