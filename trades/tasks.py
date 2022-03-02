from __future__ import absolute_import
from celery import shared_task
from django.apps import apps

from mysite.functions import *
from mysite.serializer import converter
from commons.const import *

@shared_task
def set_items(model,trade_order_id):
    seller = apps.get_model('trades',model).objects.get(pk=trade_order_id)
    seller.set_assets()
    
@shared_task
def asset_item_updater(my_to_id,target_to_id,type_id,amount):
    buyer = apps.get_model('trades',"Buyer").objects.get(pk=my_to_id)
    seller = apps.get_model('trades',"Seller").objects.get(pk=target_to_id)
    buyer.transaction_succeed(amount)
    seller.transaction_succeed(amount)
        
# @shared_task
# def wallet_updater(wallet_id,amount):
#     wallet = Wallet.objects.get(pk=wallet_id)
#     wallet.amount += amount
#     wallet.save()
    
@shared_task
def trade_order_updater(to_id,type_id,amount):
    target = apps.get_model('trades',"Trade_Order").objects.get(pk=to_id)
    result = target.자기자신을_업데이트하는_로직(type_id,amount)
    return converter(result)
