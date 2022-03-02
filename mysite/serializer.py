from datetime import datetime
from asgiref.sync import sync_to_async
from django.db.models.base import ModelState
from django.db.models import QuerySet
from channels.db import database_sync_to_async
from django.db import models
from pprint import pprint

from commons.const import *

@database_sync_to_async
def aconverter(queries:QuerySet)->dict:
    return converter(queries)

def converter(queries:QuerySet) -> dict:
    """
    querydict타입과 model타입을 구분해서 serialize해줌
    """
    if isinstance(queries,dict):#일반 dict타입일경우
        return [serialize(queries)]
        
    target:list = type_checker(queries)
    
    for obj in target:
        obj:dict = serialize(obj)
        
    #pprint(target)#debug
    if target:
        return target
    else:
        return {'message':'None Matched'}


def type_checker(queries):
    if isinstance(queries,models.Model):#Model속성일경우
        target= queries.__dict__
    elif isinstance(queries,QuerySet):
        target=list(queries.values())#Queryset - Query속성일경우
    else:
        try:
            target = queries.__dict__
        except:
            target = queries
    if isinstance(target,list):
        return target
    else:
        return [target]
    
    
def serialize(obj:dict) -> dict:
    tmp = obj.copy()
    for k,v in tmp.items():
        if isinstance(obj[k],datetime):
            obj[k] = f'{obj[k]:%Y-%m-%dT%H:%M:%S}'
        elif isinstance(obj[k],ModelState):#추상타입일경우 삭제
            del(obj[k])
        elif k =='_state':
            del(obj[k])
    return obj