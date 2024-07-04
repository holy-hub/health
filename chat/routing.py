from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/group/(?P<room_name>\w+)/$',   consumers.ChatConsumer.as_asgi()       ),
    re_path(r'ws/chat/private/(?P<room_name>\w+)/$', consumers.ChatPrivateConsumer.as_asgi()),
]