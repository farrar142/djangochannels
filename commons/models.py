# Create your models here.
from datetime import timedelta
from django.conf import settings
from django.db import models
from channels.db import database_sync_to_async
from mysite.functions import debug

if getattr(settings,"USE_TZ",False):
    from django.utils.timezone import localtime as now
else:
    from django.utils.timezone import now
class TimeMixin(models.Model):
    reg_date=models.DateTimeField('등록날짜',auto_now_add=True)
    update_date=models.DateTimeField('수정날짜',auto_now=True,null=True)
    
    class Meta:
        abstract = True
    
    def since(self):
        time = now()-self.reg_date
        return str(time)
class LogManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super().get_queryset().filter(logged_date__isnull=True)
    
    
class LogMixin(models.Model):
    
    logged_date = models.DateTimeField('로깅날짜', null=True, default=None)

    class Meta:
        abstract = True

    objects = LogManager()
    
    @classmethod
    def logging(cls,model,time=now()):
        result = model.__dict__.copy() # 인스턴스의 속성들을 카피해온다.
        del result['_state'] #인스턴스 초기화자에 포함되지 않는 속성들을 삭제한다.
        result = cls(**result) #새로운 인스턴스를 생성해준다.
        result.logged_date = time #값에 할당.
        result.save() #값을 저장
        return result #만들어진 인스턴스를 반환
       
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
    
    def __str__(self):
        return self.type
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
    def __str__(self):
        return self.code

class Event(models.Model):
    """
    1 : SIGNUP
    2 : EVENT1
    """
    event_id = models.AutoField(primary_key=True)
    event = models.CharField(max_length=100)
    
    def __str__(self):
        return self.event
    
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

