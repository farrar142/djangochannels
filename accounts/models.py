from django.db import models
from django.contrib.auth.models import AbstractUser
from products.models import Product
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
    
class Asset(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('수량')
    price = models.IntegerField('매입가')
    reg_date = models.DateTimeField('매입날짜', auto_now_add=True)

