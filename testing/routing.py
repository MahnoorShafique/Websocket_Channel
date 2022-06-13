from django.urls import path
from . import consumers


ws_patterns=[
    path('ws/sc/',consumers.MySyncConsumer.as_asgi()),
path('ws/ac/',consumers.MySyncConsumer.as_asgi())
]