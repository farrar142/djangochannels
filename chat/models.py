from django.db import models
from django.contrib.auth import get_user_model  
# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=20,unique=True)
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    def __str__(self):
        return self.name
class Messages(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True,blank=True)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    message = models.TextField()
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)