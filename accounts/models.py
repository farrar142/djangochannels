from django.db import models
from django.contrib.auth.models import AbstractUser
from products.models import Product
from market.models import *
from commons.models import *
from mysite.const import *
class User(AbstractUser):
    """
    패스워드는 상속
    """
    username = models.CharField(
        '유저이름',
        max_length=20,
        unique=True,
        help_text='20자 이하로 작성해주세요 @/./+/-/_ 를 사용 할 수 있습니다..'
    )
    email = models.EmailField('이메일')

    def custom_save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        Points(user=self,cur_point=100000).save()
        PointsHistories(user=self,point=100000,event_id=SIGNUP).save()

class Points(models.Model):
    user = models.OneToOneField(User,on_delete=models.DO_NOTHING,related_name='point')
    cur_point = models.IntegerField(null=True,blank=True)
    
class PointsHistories(models.Model):
    user = models.OneToOneField(User,on_delete=models.DO_NOTHING,related_name='pointhistories')
    point = models.IntegerField(null=True,blank=True)
    event = models.ForeignKey(Event,on_delete=models.DO_NOTHING)
    
class Asset(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    
    @classmethod    
    @database_sync_to_async
    def get_asset(cls,user_id,product_id):
        asset,is_created = Asset.objects.get_or_create(user_id=user_id,product_id=product_id)
        print(asset)
        return asset