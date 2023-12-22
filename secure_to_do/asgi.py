import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secure_to_do.dev_settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from to_do_app.routing import websocket_urlpatterns


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": 
        URLRouter(
            websocket_urlpatterns
        )
    ,
})