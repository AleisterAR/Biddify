"""
ASGI config for keister_house project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack
import bid.routing as bid_route 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keister_house.settings')

application = ProtocolTypeRouter(
    {'http': get_asgi_application(),
     'websocket': AuthMiddlewareStack(
         URLRouter(
             bid_route.websocket_urlpatterns
         )
     )
     }
)
