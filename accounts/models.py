from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
class User(AbstractUser):
    """
    패스워드는 상속
    """
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        '유저이름',
        max_length=20,
        unique=True,
        help_text='20자 이하로 작성해주세요 @/./+/-/_ 를 사용 할 수 있습니다..',
        validators=[username_validator],
        error_messages={
            'unique': "중복되는 이름이 있습니다.",
        },
    )
    email = models.EmailField('이메일')
    
class ProductCategory(models.model):
    name = models.CharField('종목이름',max_length=20,unique=True)
    
class Product(models.model):
    """
    기업규모,재정건전성,산업종류[1차,2차,3차,4차] ...
    """
    name = models.CharField('상품이름',max_length=20,unique=True)
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE)#CASCADE = ForeignKey(일대다 모델의 참조키)삭제시 자동으로 인스턴스 삭제
    quantity = models.PositiveIntegerField('총수량')
    price = models.IntegerField('현재가')
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True,null=True,blank=True)
    
class ProductLog(models.model):
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)#DO_NOTHING = ForeignKey삭제시 삭제 안됨.
    p_name = models.CharField("상품이름",max_length=20)
    quantity = models.PositiveIntegerField('총수량')
    price = models.IntegerField('가격')
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    
class Asset(models.model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('수량')
    price = models.IntegerField('매입가')
    reg_date = models.DateTimeField('매입날짜', auto_now_add=True)

class Trade(models.model):
    class TradeTypeChoice(models.TextChoices):
        SELL = "매도"
        BUY = "매입"
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.IntegerField('거래가격')
    status = models.CharField('거래유형', max_length=20, choices=TradeTypeChoice.choices)
    reg_date = models.DateTimeField('게시날짜', auto_now_add=True)
    
class TradeLog(models.model):    
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    u_name = models.CharField("유저이름",max_length=20)
    p_name = models.CharField("상품이름",max_length=20)
    price = models.IntegerField('거래가격')
    status = models.CharField('거래유형')
    reg_date = models.DateTimeField('게시날짜', auto_now_add=True)