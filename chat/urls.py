# chat/urls.py
from django.urls import path

from . import views
from . import tasks
app_name = "chat"
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('<str:room_name>/add', tasks.message_add, name='message_add'),
    path('<str:room_name>/remove', tasks.room_remove, name='room_remove'),
]