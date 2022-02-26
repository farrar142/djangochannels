# Create your models here.
from datetime import timedelta
from django.db import models
from django.utils import timezone
from channels.db import database_sync_to_async
from mysite.functions import debug
class TimeMixin(models.Model):
    reg_date=models.DateTimeField('등록날짜',auto_now_add=True)
    update_date=models.DateTimeField('수정날짜',auto_now=True,null=True)
    
    class Meta:
        abstract = True
    
    def since(self):
        time = timezone.now()-self.reg_date
        return str(time)
    
class AsyncModel(TimeMixin):
    @database_sync_to_async
    def async_save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        return self
    
    @classmethod    
    @database_sync_to_async
    def async_bulk_post(cls,amount:int,**kwargs):
        result = [cls(**kwargs) for i in range(amount)]
        result = cls.objects.bulk_create(result)
        result = [i.pk for i in result]
        result = cls.objects.filter(pk__in = result)
        return result
    
    @classmethod    
    @database_sync_to_async
    def async_create(cls,**kwargs):
        result = cls(**kwargs)
        result.save()
        return result
    
    @classmethod    
    @database_sync_to_async
    def async_get(cls,**kwargs):
        result = cls.objects.get(**kwargs)
        return result
    
    class Meta:
        abstract = True

class Type(models.Model):
    """
    BUY
    SELL
    """
    type_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20)
#
class Code(models.Model):
    """
    1 : NORM
    2 : COMP
    3 : CANC
    ---------
    4 : HOLD
    5 : STOCK
    """
    code_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20)

class Event(models.Model):
    """
    1 : SIGNUP
    2 : EVENT1
    """
    event_id = models.AutoField(primary_key=True)
    event = models.CharField(max_length=100)
    
    
"""
ASSETITEM LIFECYCLE

(미보유상태      INSERT-> BUY MARKET)

BUY     MARKET  =   미보유 / 구매전
(BUY MARKET     UPDATE  -> BUY HOLD)

        HOLD    =   보유중 / 구매후
(BUY HOLD       UPDATE  ->  SELL MARKET)
        
SELL    MARKET  =   보유중 / 판매중
(SELL MARKET -> DELETE)
"""

