import json

import uuid
import redis
import threading
import logger

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.resource import Resource, WebSocketApplication

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
CHANNEL_DISPATCH = 'msg'
CHANNEL_SOCKET = 'room1'

class RedisBroker():
    def __init__(self):
        self.sockets = {}

    def subscribe(self, key, socket):
        if key not in self.sockets:
            self.sockets[key] = set()

        if socket in self.sockets[key]:
            return

        self.sockets[key].add(socket)

    def publish(self, key, data):
        if key not in self.sockets:
            return
        
        for socket in self.sockets[key]:
            socket.on_broadcast(json.loads(bytes.decode(data)))

    def unsubscribe(self, key, socket):
        if key not in self.sockets: return

        self.sockets[key].remove(socket)

broker = RedisBroker()


class Chat(WebSocketApplication):

    def on_open(self, *args, **kwargs):
        self.userid = uuid.uuid4()
        broker.subscribe(CHANNEL_SOCKET, self)

    def on_close(self, *args, **kwargs):
        broker.unsubscribe(CHANNEL_SOCKET, self)

    def on_message(self, message, *args, **kwargs):
        if not message: return

        data = json.loads(message)
        data['user'] = self.userid.hex
        publish(data)
        logger.debug('receive:%s from %s' % (data['message'], data['user']))

    def on_broadcast(self, data):
        self.ws.send(json.dumps(data))
        
def callback():
    r = redis.client.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    sub = r.pubsub()
    sub.subscribe(CHANNEL_DISPATCH)
    while True:
        for topic in sub.listen():
            broker.publish(CHANNEL_SOCKET, topic['data'])
            
def publish(data):
    r = redis.client.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    r.publish(CHANNEL_DISPATCH, json.dumps(data))


def index(environ, start_response):
    start_response('200 OK', [('Content-type','text/html')])
    html = open('index.html', 'rb').read()
    return [html]


application = Resource([
    ('^/chat', Chat),
    ('^/', index)
])


if __name__ == '__main__':
    t = threading.Thread(target=callback)
    t.setDaemon(True)
    t.start()
    WSGIServer('{}:{}'.format('0.0.0.0', 8000), application, handler_class=WebSocketHandler).serve_forever()

