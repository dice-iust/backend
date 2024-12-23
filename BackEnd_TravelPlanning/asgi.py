import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import path
from chat import consumers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BackEnd_TravelPlanning.settings")
django.setup()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path(
                        "ws/chat/<str:travel_name>/", consumers.ChatConsumer.as_asgi()
                    ),
                ]
            )
        ),
    }
)
ASGI_APPLICATION = 'BackEnd_TravelPlanning.asgi.application'