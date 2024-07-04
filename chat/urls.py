from django.urls import path
from .views      import *

urlpatterns = [
    path("group/<str:room_name>/", chat_room, name="room"),
    path("private/<str:room_name>/", chat_private_room, name="privateRoom"),
]