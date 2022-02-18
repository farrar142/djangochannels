# mysite/urls.py

from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.conf import settings
from .views import *
from .api import api
import debug_toolbar
urlpatterns = [
    path('',index,name='index'),
    path('test',test,name='test'),
    path('accounts/',include('accounts.urls')),
    path('chat/', include('chat.urls')),
    path('trades/', include('trades.urls')),
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('__debug__/', include(debug_toolbar.urls)),
]
