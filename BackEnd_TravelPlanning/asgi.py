# your_project/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns  # Make sure this imports your routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BackEnd_TravelPlanning.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns  # Make sure the correct URL patterns are passed
            )
        ),
    }
)
