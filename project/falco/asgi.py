import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "falco.settings")

import django
django.setup()

from channels.auth import AuthMiddlewareStack 
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import OriginValidator , AllowedHostsOriginValidator
from channels.sessions import SessionMiddlewareStack
from messenger import routing

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
  "http": django_asgi_app,
  "websocket": AllowedHostsOriginValidator(
      SessionMiddlewareStack(
        AuthMiddlewareStack(
          URLRouter(
            routing.websocket_urlpatterns
          )
        )
      ) 
    )
})
