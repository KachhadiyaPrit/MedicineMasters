"""
ASGI config for medicinemasters project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from django.core.asgi import get_asgi_application
from medicine_masters.consumers import *
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicinemasters.settings')

application = get_asgi_application()

ws_pattern = [
    path('ws/track_order_detail/<order_tracking_id>', OrderProgress.as_asgi()),
    path('ws/new/', NewConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket" : AuthMiddlewareStack(URLRouter(
        ws_pattern
    ))
})