from gevent import monkey
monkey.patch_all()  # monkey patch for gevent

import gevent
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketHandler, WebSocketError
import json
import base64
from bottle import request, Bottle, abort
from bottle_redis import RedisPlugin

from .impl.test import getTestSessionInfo, getTestLiveSnaps
from .config import REDIS_HOST, REDIS_PORT, WEB_HOST, WEB_PORT  # import db configuration

appws = Bottle()
redis_plugin = RedisPlugin(host=REDIS_HOST,
                           port=REDIS_PORT,
                           database=0,
                           keyword='rdb')
appws.install(redis_plugin)  # install redis plugin


@appws.route('/group/<gid>/test/<sid>/screen')
def handle_screen_websocket(gid, sid):
    '''
    @deprecated
    '''
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    ret = getTestSessionInfo(gid, sid)
    if not ret is None:
        # wslist[sid].append({'ws':wsock, 'snaptime':''})
        deviceinfo = ret['results']['deviceinfo']
        wsock.send('snapsize:' + json.dumps(deviceinfo))
    else:
        abort(404, 'Request device is invalid.')
    
    def send_screed():
        timestamp = None
        while True:
            try:
                snapdata = ''
                snaps = getTestLiveSnaps(gid, sid, timestamp)
                lenf = len(snaps)
                if lenf > 0:
                    timestamp = snaps[lenf - 1]['snaptime']
                    snapdata = base64.encodestring(snaps[lenf - 1]['snap'])
                    wsock.send('snapshot:' + snapdata)
                gevent.sleep(0.3)
            except WebSocketError:
                break
    g = gevent.spawn(send_screed)
    while True:
        try:
            message = wsock.receive()
            # handle received message from client
            if message is None:
                break
        except WebSocketError:
            break
    g.kill()  # kill redis subscribing process


@appws.route('/group/<gid>/test/<sid>/snapshot')
def ws_snapshot(gid, sid, rdb):
    '''
    This is just an example for how to async process redis pubsub and websocket.
    '''
    ws = request.environ.get('wsgi.websocket')
    if ws is None:
        abort(400, 'Expected WebSocket request.')

    def redis_sub():
        ps = rdb.pubsub()
        # subscribe channel....
        ps.subscribe("my")
        for msg in ps.listen():
            # Handle message published in subscribed channel and then
            # send data via websocket in case of needed
            # The published msg has 4 fields:
            # msg.pattern: pattern you subscribed via psubscribe, None if you r using subscribe
            # msg.type: you only need to process data in case of type == 'message'
            # msg.channel: the channel of the message
            # msg.data: the message data
            ws.send("Publish message: %s" % msg)

    # start to greenlet to process subscribed message async.
    g = gevent.spawn(redis_sub)
    while True:
        try:
            message = ws.receive()
            # handle received message from client
            if message is None:
                break
            ws.send("The message you got is %s" % message)
        except WebSocketError:
            break
    g.kill()  # kill redis subscribing process


def main():
    port = WEB_PORT
    host = WEB_HOST
    print 'LiveStream Serving on %s:%d...' % (host, port)
    WSGIServer((host, port), appws, handler_class=WebSocketHandler).serve_forever()


if __name__ == '__main__':
    main()
