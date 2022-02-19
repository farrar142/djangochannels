from django.db import models
from django.contrib.auth.models import AbstractUser
from commons.models import *
from commons.const import *
#
class User(AbstractUser):
    """
    패스워드는 상속
    """
    class Meta:
        db_table = "accounts_user"
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(
        '유저이름',
        max_length=20,
        unique=True,
        help_text='20자 이하로 작성해주세요 @/./+/-/_ 를 사용 할 수 있습니다..'
    )
    email = models.EmailField('이메일')

    def custom_save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        Point(user=self,cur_point=100000).save()
        Point_History(user=self,point=100000,event_id=SIGNUP).save()

class Point(models.Model):
    class Meta:
        db_table = "accounts_point"
    point_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.DO_NOTHING,related_name='point')
    cur_point = models.IntegerField(null=True,blank=True)
    
class Point_History(models.Model):
    class Meta:
        db_table = "accounts_point_history"
    point_history_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.DO_NOTHING,related_name='pointhistories')
    point = models.IntegerField(null=True,blank=True)
    event = models.ForeignKey(Event,on_delete=models.DO_NOTHING)
    
# class Asset(models.Model):
#     class Meta:
#         db_table = "accounts_asset"
#     asset_id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     product = models.ForeignKey('stocks.product',on_delete=models.CASCADE)
    
#     @classmethod    
#     @database_sync_to_async
#     def get_asset(cls,user_id,product_id):
#         asset,is_created = Asset.objects.get_or_create(user_id=user_id,product_id=product_id)
#         print(asset)
#         return asset