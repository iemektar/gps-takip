from channels.routing import route
from location.consumer import *
channel_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.disconnect',ws_disconnect),
]