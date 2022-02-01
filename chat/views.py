# chat/views.py
from django.http import JsonResponse
from django.shortcuts import render,redirect
from .models import *
from .tasks import *

def index(request):
    rooms = Room.objects.all()
    context={'rooms':rooms}
    return render(request, 'chat/index.html',context)
        
def room(request, room_name):
    room_name = ''.join(char for char in room_name if char.isalnum())
    rooms = Room.objects.all()
    room = Room.objects.filter(name=room_name).first()
    if not room:
        if room_name != "":
            room = Room(name=room_name)
            room.save()
        return redirect('chat:index')
    else:
        messages = room.messages_set.filter(room=room)
        logs = ''
        if messages:
            for message in messages:
                if message.user:
                    cur_user = message.user.username
                else:
                    cur_user = "낯선상대"
                logs = f"{cur_user} : {message.message}\n" + logs
        clean_message.delay(room.id).get()
        get_flexible_models.delay('room')
        context={'rooms':rooms,'room': room,'messages':logs}
        return render(request, 'chat/room.html', context)
