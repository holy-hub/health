from django.urls import path
from .views import *

urlpatterns = [
    path("<str:room_name>/", chat_room, name="room"),
]