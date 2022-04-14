from django.urls import re_path , path
from root.consumer import ChatRoom,adminAlert

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_id>\w+)/$",ChatRoom.as_asgi()),
    path('ws/alert/',adminAlert.as_asgi())
]