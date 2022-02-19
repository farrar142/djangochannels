from datetime import datetime
from asgiref.sync import sync_to_async
from django.db.models.base import ModelState
from django.db.models import QuerySet
from channels.db import database_sync_to_async
from django.db import models
from pprint import pprint

from commons.const import *

@database_sync_to_async
def converter(queries:QuerySet) -> dict:
    """
    querydict타입과 model타입을 구분해서 serialize해줌
    """
    if isinstance(queries,dict):#일반 dict타입일경우
        return serialize(queries)
        
    target:list = type_checker(queries)
    
    for obj in target:
        obj:dict = serialize(obj)
        
    #pprint(target)#debug
    if target:
        #target이 system메세지일경우 target["system"]
        result = {}
        system = {
            'result':SUCCEED,
            'messages':SUCCEED
        }
        result.update(system=system)
        result.update(datas=target)
        return result
    else:
        return{
                "system":{
                'result':NONE,
                'messages':NONE
                }
            }

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

def type_checker(queries):
    if isinstance(queries,models.Model):#Model속성일경우
        target= [queries.__dict__]
    elif isinstance(queries,QuerySet):
        if isinstance(queries.first(),dict):#Queryset - QueryDict속성일경우
            target = list(queries)
        else:
            target=list(queries.values())#Queryset - Query속성일경우
    else:
        target = queries
    return target