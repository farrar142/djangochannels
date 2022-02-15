from __future__ import absolute_import

import datetime
from django.shortcuts import get_object_or_404
from celery import shared_task
    
@shared_task
def add(x,y):
    print("tasks")
    return x+y