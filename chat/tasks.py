from __future__ import absolute_import

import datetime

from celery import shared_task
from django.template import loader
from django.utils import timezone
from django.apps import apps
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render,redirect
from asgiref.sync import sync_to_async
from .models import *

@shared_task
def room_remove(request,room_name):
    room = Room.objects.get(name=room_name).delete()
    return redirect('chat:index')

@shared_task
def message_add(request,room_name):
    """
    for logging
    """
    room = Room.objects.get(name=room_name)
    username=request.GET['username']
    message = request.GET['message']
    if request.user.is_authenticated:
        Messages(user=request.user,room=room,message=message).save()
    else:
        Messages(room=room,message=message).save()
    return JsonResponse({
        'resultCode':"S-1",
        'username':username,
        'message':message,
    })

@shared_task
def get_rooms():
    from chat.models import Room
    return Room.objects.all()

@shared_task
def clean_message(room_id):
    room = Room.objects.get(id=room_id)
    Messages.objects.filter(reg_date__lt=timezone.now()-datetime.timedelta(days=2),
                            room=room).delete()

@shared_task
def get_flexible_models(model_name):
    Model = apps.get_model(f'chat.{model_name}')
    obj = Model.objects.all()
    return list(obj.values())
