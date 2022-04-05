from __future__ import absolute_import
from celery import shared_task
from django.apps import apps
from django.conf import settings
from .models import Product

if getattr(settings,"USE_TZ",False):
    from django.utils.timezone import localtime as now
else:
    from django.utils.timezone import now
    
    
@shared_task
def logging_product():
    targets = Product.objects.all()
    [i.logging() for i in targets]