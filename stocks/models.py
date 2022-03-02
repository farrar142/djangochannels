from django.db import models
from commons.models import *
# Create your models here.

class Product_Category(models.Model):
    class Meta:
        db_table = "stocks_product_category"
    product_category_id = models.AutoField(primary_key=True)
    name = models.CharField('종목이름',max_length=20,unique=True)
    def __str__(self):
        return str(self.name)
    
class ProductMixin(AsyncModel):
    class Meta:
        abstract = True
    product_id = models.AutoField(primary_key=True)
    name = models.CharField('상품이름',max_length=20,unique=True)
    category = models.ForeignKey(Product_Category,on_delete=models.CASCADE)
    # yester_end_price = models.IntegerField('전일종가',null=True,blank=True,default=0)
    # yester_quantity = models.IntegerField('전일거래량',null=True,blank=True,default=0)
    start_price = models.IntegerField('당일시가',null=True,blank=True,default=0)
    end_price = models.IntegerField('당일종가',null=True,blank=True,default=0)
    #종가는 계속 업데이트됨.
    max_price = models.IntegerField('고가',null=True,blank=True,default=0)
    min_price = models.IntegerField('저가',null=True,blank=True,default=0)
        
    def __str__(self):
        return f"[{self.category}] : {self.name}"
    
class ProductLogManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super().get_queryset().filter(logged_date__isnull=False)
    
class ProductLog(ProductMixin,LogMixin):
    class Meta:
        db_table = "stocks_product_log"
    objects=ProductLogManager()
    
class Product(ProductMixin):
    class Meta:
        db_table = "stocks_product"
    
    def logging(self,time=timezone.now()):
        result = self.__dict__.copy()
        del result['_state']
        result = ProductLog(**result)
        result.logged_date=time
        self.start_price=self.end_price
        self.max_price=0
        self.min_price=0
        self.save()
        result.save()
        
    def monitoring(self,amount):
        self.set_max_price(amount)
        self.set_min_price(amount)
        self.save()
    def end_price(self):
        pass
    
    def set_max_price(self,amount):
        if self.max_price <= amount:
            self.max_price = amount
    def set_min_price(self,amount):
        if self.min_price >= amount:
            self.min_price = amount