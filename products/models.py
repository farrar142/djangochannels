from django.db import models
from commons.models import *
# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField('종목이름',max_length=20,unique=True)
    def __str__(self):
        return str(self.name)
    
class Product(AsyncModel):
    """
    기업규모,재정건전성,산업종류[1차,2차,3차,4차] ...
    """
    name = models.CharField('상품이름',max_length=20,unique=True)
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE)#CASCADE = ForeignKey(일대다 모델의 참조키)삭제시 자동으로 인스턴스 삭제
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True,null=True,blank=True)
    
    ##각 종목별 인스턴스는 하나
    ##setter로 수정 후 매일마다(celeryTask이용) ProductLog로 전환
    yester_end_price = models.IntegerField('전일종가',null=True,blank=True,default=0)
    yester_quantity = models.IntegerField('전일거래량',null=True,blank=True,default=0)
    start_price = models.IntegerField('당일시가',null=True,blank=True,default=0)
    start_price = models.IntegerField('당일종가',null=True,blank=True,default=0)
    max_price = models.IntegerField('고가',null=True,blank=True,default=0)
    max_price = models.IntegerField('저가',null=True,blank=True,default=0)
        
    
    def __str__(self):
        return f"[{self.category}] : {self.name}"
    
class ProductLog(models.Model):
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)#DO_NOTHING = ForeignKey삭제시 삭제 안됨.
    p_name = models.CharField("상품이름",max_length=20)
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    
    yester_end_price = models.IntegerField('전일종가',null=True,blank=True,default=0)
    yester_quantity = models.IntegerField('전일거래량',null=True,blank=True,default=0)
    start_price = models.IntegerField('당일시가',null=True,blank=True,default=0)
    start_price = models.IntegerField('당일종가',null=True,blank=True,default=0)
    max_price = models.IntegerField('고가',null=True,blank=True,default=0)
    max_price = models.IntegerField('저가',null=True,blank=True,default=0)
    