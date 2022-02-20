from __future__ import absolute_import
from datetime import datetime

from celery import shared_task
from django.db import connection
from commons.const import *
from assets.models import *
from mysite.functions import *


@shared_task
def asset_item_bulk_updater(trade_order_id,code_id,type_id,product_id,user_id,quantity,target=['code_id','type_id','trade_order_id']):
    
    update = f"""
    update asset_item set code_id={MARKET},type_id={SELL},trade_order_id={trade_order_id} where product_id = {product_id} and user_id={user_id} and code_id={HOLD} and type_id={BUY} limit {quantity} 
    """
    
    with connection.cursor() as cursor:
        cursor.execute(update)
    # items = Asset_Item.objects.filter(pk__in =items)
    # for item in items:
    #     item.code_id = MARKET
    #     item.type_id = SELL
    #     item.trade_order_id = trade_order_id
        
    # Asset_Item.objects.bulk_update(items,target)
    
@shared_task
def asset_item_bulk_creater(user_id,product_id,trade_order_id,point,quantity):
    cur_time = datetime.now()
    cur_time_format = f"{cur_time:%Y-%m-%d %H:%M:%S}"
    target = [(user_id,product_id,trade_order_id,MARKET,BUY,point,cur_time_format)for i in range(0,quantity)]
    
    multiple_row_insert =f"""
    insert into asset_item 
    (user_id,product_id,trade_order_id,code_id,type_id,point,reg_date) values {value_parser(target)}
    """
    with connection.cursor() as cursor:
        cursor.execute(multiple_row_insert)
    # Asset_Item.objects.bulk_create(##db hit 1
    #         [Asset_Item(user_id=user_id,product_id=product_id,trade_order_id=trade_order_id,code_id=MARKET,type_id=BUY,point=point) for i in range(0,quantity) ]
    #     )
    
@shared_task
def asset_item_updater(target_to_id,my_to_id,type_id,amount):
    
    if type_id == BUY:
        status_updater(my_to_id,target_to_id,amount)
    elif type_id == SELL:
        status_updater(target_to_id,my_to_id,amount)
    
def status_updater(update_to_id,delete_order_id,amount):
    print("here inner function")
    
    # update_items = Asset_Item.objects.filter(trade_order_id=update_to_id,code_id=MARKET)[:amount]
    # limiter = 0
    # while(update_items.count()==0):
    #     time.sleep(1)
    #     update_items = Asset_Item.objects.filter(trade_order_id=update_to_id,code_id=MARKET)[:amount]
    #     limiter += 1
    #     if limiter >=60:
    #         break;
    # for items in update_items:
    #     items.code_id = HOLD
        
        
    update = f"""
    update asset_item set code_id={HOLD} where trade_order_id = {update_to_id} and code_id={MARKET} limit {amount} 
    """
        
    #count = Asset_Item.objects.bulk_update(update_items,['code_id'])
    delete = f"delete from asset_item where trade_order_id = {delete_order_id} and code_id = {MARKET} limit {amount}"
    # print(query)
    # Asset_Item.objects.raw(query)
    with connection.cursor() as cursor:
        cursor.execute(update)
        cursor.execute(delete)
    
    # delete_ids = [item.pk for item in delete_items]
    # delete_items = Asset_Item.objects.filter(pk__in = delete_ids)
    # delete_items.delete()
@shared_task
def wallet_updater(wallet_id,amount):
    wallet = Wallet.objects.get(pk=wallet_id)
    wallet.amount += amount
    wallet.save()