import os

from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import message.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AndroidApi.settings')

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            message.routing.websocket_urlpatterns
        )
    ),
})