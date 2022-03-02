from django.db import models
from django.db.models import *
from django.db.models.manager import Manager
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

class Wallet(User):        
    class Meta:
        proxy = True
        
    class mock(dict):
        def __init__(self,p_id):
            self.update(product_id = p_id)
            self.update(product_name = None)
            self.update(amount = 0)
    @property
    def my_stocks(self):
        return self.asset_item.values('product_id').annotate(
            product_name=F('product__name'),amount=Count("product")
            )
        
    @property
    def my_all_stocks(self):
        return self.my_stocks.filter(
                Q(code_id=HOLD,type_id=BUY)|Q(code_id=MARKET,type_id=SELL)
            )
            
    def my_selling_stocks(self,product_id):
    
        result = self.my_stocks.filter(
                Q(code_id=MARKET,type_id=SELL,product_id=product_id)
            )
        if len(result)>0:
            return result[0]
        else:
            return self.mock(product_id)
        
    def my_holding_stocks(self,product_id):
        result =  self.my_stocks.filter(
                Q(code_id=HOLD,type_id=BUY,product_id=product_id)
            )
        if len(result)>0:
            return result[0]
        else:
            return self.mock(product_id)
class Point(AsyncModel):
    class Meta:
        db_table = "accounts_point"
    point_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.DO_NOTHING,related_name='point')
    cur_point = models.IntegerField(null=True,blank=True)
    
class Point_History(AsyncModel):
    class Meta:
        db_table = "accounts_point_history"
    point_history_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.DO_NOTHING,related_name='pointhistories')
    point = models.IntegerField(null=True,blank=True)
    event = models.ForeignKey(Event,on_delete=models.DO_NOTHING)
    