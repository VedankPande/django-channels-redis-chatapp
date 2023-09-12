from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("chat/send/<str:target>", consumers.ChatConsumer.as_asgi()),
]