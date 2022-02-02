from django.db import models
from accounts.models import User
from products.models import Product
# Create your models here.
class Trade(models.Model):
    class TradeTypeChoice(models.TextChoices):
        SELL = "매도"
        BUY = "매입"
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.IntegerField('거래가격')
    status = models.CharField('거래유형', max_length=20, choices=TradeTypeChoice.choices)
    reg_date = models.DateTimeField('게시날짜', auto_now_add=True)
    
class TradeLog(models.Model):    
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    u_name = models.CharField("유저이름",max_length=20)
    p_name = models.CharField("상품이름",max_length=20)
    price = models.IntegerField('거래가격')
    status = models.CharField('거래유형',max_length=20)
    reg_date = models.DateTimeField('게시날짜', auto_now_add=True)