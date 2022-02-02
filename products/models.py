from django.db import models

# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField('종목이름',max_length=20,unique=True)
    def __str__(self):
        return str(self.name)
    
class Product(models.Model):
    """
    기업규모,재정건전성,산업종류[1차,2차,3차,4차] ...
    """
    name = models.CharField('상품이름',max_length=20,unique=True)
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE)#CASCADE = ForeignKey(일대다 모델의 참조키)삭제시 자동으로 인스턴스 삭제
    quantity = models.PositiveIntegerField('총수량')
    price = models.IntegerField('현재가')
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True,null=True,blank=True)
    def __str__(self):
        return f"[{self.category}] : {self.name}"
    
class ProductLog(models.Model):
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)#DO_NOTHING = ForeignKey삭제시 삭제 안됨.
    p_name = models.CharField("상품이름",max_length=20)
    quantity = models.PositiveIntegerField('총수량')
    price = models.IntegerField('가격')
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    