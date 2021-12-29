from message import consumers_chat, consumers_notif
from django.urls import re_path

from . import *

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/(?P<srcId>\w+)/(?P<destId>\w+)$', consumers_chat.ChatConsumer.as_asgi()),
    re_path(r'ws/notif/(?P<room_name>\w+)$', consumers_notif.ChatConsumer.as_asgi()),
]