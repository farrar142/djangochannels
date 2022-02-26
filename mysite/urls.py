# mysite/urls.py

from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.conf import settings
from .views import *
from .api import api
from custommiddle.urls import api as test_api
import debug_toolbar
urlpatterns = [
    path('',index,name='index'),
    path('test',test,name='test'),
    path('token/',test_api.urls),
    path('accounts/',include('accounts.urls')),
    path('chat/', include('chat.urls')),
    path('trades/', include('trades.urls')),
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),

#         # For django versions before 2.0:
#         # url(r'^__debug__/', include(debug_toolbar.urls)),

#     ] + urlpatterns