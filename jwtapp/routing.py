from django.urls import path
from jwtapp.consumers import TestConsumer, NewConsumer
from channels.routing import ProtocolTypeRouter, URLRouter

ws_patterns = [
        path("ws/test/", TestConsumer),
        path("ws/new-test/", NewConsumer),
]
