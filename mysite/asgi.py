import os,django

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter,get_default_application
from channels.security.websocket import OriginValidator
from django.core.asgi import get_asgi_application
from django.urls import re_path,path
from . import routing
from chat import consumers

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
#application = get_default_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": OriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
                
            )
        ),
        ["*"],
    )
})