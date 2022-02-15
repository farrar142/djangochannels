from django.db import models

# Create your models here.
from django.db import models
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

class AsyncModel(models.Model):
    @database_sync_to_async
    def async_save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        return self
    class Meta:
        abstract = True

class Type(models.Model):
    """
    BUY
    SELL
    """
    type = models.CharField(max_length=20)

class Code(models.Model):
    """
    NORM
    COMP
    CANC
    """
    code = models.CharField(max_length=20)

class Event(models.Model):
    event = models.CharField(max_length=100)