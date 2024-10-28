from django.urls import re_path
from .consumers import LogConsumer
websocket_urlpatterns = [
    re_path(r'log/$', LogConsumer.as_asgi()),
]