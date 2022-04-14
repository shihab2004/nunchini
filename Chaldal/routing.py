from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from root.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
 "websocket": AllowedHostsOriginValidator(
    AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
 )
})
