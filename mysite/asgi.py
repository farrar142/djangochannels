# mysite/asgi.py
import os,django

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter,get_default_application
from django.core.asgi import get_asgi_application
from . import routing

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
#application = get_default_application()
application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})