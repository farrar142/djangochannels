# mysite/urls.py

from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.conf import settings
from .views import MainView
import debug_toolbar
urlpatterns = [
    path('',MainView.as_view(),name='index'),
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
]
