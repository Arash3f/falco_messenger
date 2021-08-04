from django.urls import path
from messenger import consumers

websocket_urlpatterns= [
    path('ws/messenger/<slug:slug>/' , consumers.ChatConsumer.as_asgi()),
]