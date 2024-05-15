"""
ASGI config for mindsupport project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import os
import django

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mindsupport.settings")
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path
from api.consumers import TextRoomConsumer

websocket_urlpatterns = [
    re_path(r"^ws/(?P<sala>[^/]+)/$", TextRoomConsumer.as_asgi()),
]

application = ProtocolTypeRouter(
    {"http": get_asgi_application(), "websocket": URLRouter(websocket_urlpatterns)}
)
