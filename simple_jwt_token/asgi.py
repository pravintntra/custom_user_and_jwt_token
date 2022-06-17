"""
ASGI config for simple_jwt_token project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from jwtapp.routing import ws_patterns
from jwtapp.consumers import TestConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simple_jwt_token.settings")

application = get_asgi_application()

application = ProtocolTypeRouter({"websocket": URLRouter(ws_patterns)})
