import uuid
from datetime import timedelta
from django.db import models
from django.conf import settings
from django.http import HttpRequest
from django.utils import timezone

class Token(models.Model):
    token = models.TextField('token')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    expired_in = models.DateTimeField()
    UNIT_OF_TIME = "hours"
    TIMES= 1
    class Meta:
        db_table = "token"
    
    def __init__(self,*args, **kwargs):
        
        self.PREFIX                 = getattr(settings,"CUSTOM_PREFIX",'')
        if self.PREFIX:
            self.PREFIX += "_"
        self.TIMES                  = getattr(settings,f"{self.PREFIX}TIMES",1)
        self.UNIT_OF_TIME           = getattr(settings,f"{self.PREFIX}UNIT_OF_TIME",'hours')
        super().__init__(*args,**kwargs)
        
    
    @classmethod
    def get_or_create(cls,token,user_id):
        try:
            try:
                return Token.objects.get(token=token)
            except:
                return Token.objects.get(user_id=user_id)
        except:
            return Token.objects.create(
                token=cls.token_generator(),
                user_id=user_id,
                expired_in=cls.suspended_time()
                                 )
    @classmethod
    def token_refresher(cls,token):
        token.expired_in = cls.suspended_time()
        token.save()
        print('token refreshed')
        return token
    @classmethod
    def token_generator(cls):
        return str(uuid.uuid4())
        
    @classmethod
    def suspended_time(cls):
        print(cls.UNIT_OF_TIME,cls.TIMES)
        polling_time = {cls.UNIT_OF_TIME:cls.TIMES}
        return timezone.now()+timedelta(**polling_time)