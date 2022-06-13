
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

import chnl_lyr.routing
import dbinChnl.routing
import testing.routing
import chnl_lyr.routing
from testing.consumers import *
from channels.auth import AuthMiddlewareStack
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'channel_practice.settings')

# application = get_asgi_application()
# ws_patterns=[
#     path("ws/test/",TestConsumer.as_asgi())
# ]

application=ProtocolTypeRouter({
    'http':get_asgi_application(),
    # 'websocket':URLRouter(
    #     # testing.routing.ws_patterns,
    #     # chnl_lyr.routing.ws_patterns_chnl
    #
    #   dbinChnl.routing.ws_patterns_dbchnl
    #
    # )

    # for implementing auth
'websocket':AuthMiddlewareStack(URLRouter(dbinChnl.routing.ws_patterns_dbchnl))
})