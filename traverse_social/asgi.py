import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "traverse_social.settings")
django.setup()

from tweets.consumers import MyConsumer
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack


from chat.consumers import ChatConsumer
from .channelsmiddleware import TokenAuthMiddlewareStack




application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": get_asgi_application(),

    # WebSocket chat handler
    "websocket": TokenAuthMiddlewareStack(
        URLRouter([
             path('ws/chat/<str:username>/',ChatConsumer.as_asgi()),
            path('ws/home/', MyConsumer.as_asgi()),
           
        ])
    ),
})