from django.urls import re_path
from .consumers import LogConsumer, ServiceLogConsumer
websocket_urlpatterns = [
    re_path(r'log/$', LogConsumer.as_asgi()),
    re_path(r'serviceLogs/$', ServiceLogConsumer.as_asgi())
]