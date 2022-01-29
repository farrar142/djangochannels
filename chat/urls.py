# chat/urls.py
from django.urls import path

from . import views
app_name = "chat"
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('<str:room_name>/add', views.message_add, name='message_add'),
    path('<str:room_name>/remove', views.room_remove, name='room_remove'),
]