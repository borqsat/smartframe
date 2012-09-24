from bottle import request, response, Bottle, abort
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketHandler, WebSocketError
from impl.test import *
from impl.device import *
from impl.auth import *
import json, base64, time, threading

appws = Bottle()
@appws.route('/test/session/<sid>/screen')
def handle_screen_websocket(sid):
    print 'handle snapshot request...'
    token = '1122334455667788'
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    else:
        wsock.send('snapsize:{"width":"600px","height":"1024px"}')

    while True:
        try:
            message = wsock.receive()
            snaplive = getTestSessionSnaps(token, sid)
            lenf = len(snaplive)
            msgdata = 'nop'
            if lenf > 0:
                msgdata = 'snapshot:' + base64.encodestring(snaplive[lenf-1])
            time.sleep(0.3)
            wsock.send(msgdata)
        except WebSocketError:
            break

@appws.route('/test/session/<sid>/terminal')
def handle_console_websocket(sid):
    token = '1122334455667788'
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    else:
        wsock.send('nop')

    while True:
        try:
            message = wsock.receive()
            testlive = getTestSessionResults(token, sid)
            lenf = len(testlive)
            msgdata = 'nop'
            if lenf > 0:
                msgdata = 'caseupdate:' + testlive[lenf-1]
            time.sleep(1)
            wsock.send(msgdata)
        except WebSocketError:
            break

if __name__ == '__main__':
    WSGIServer(("", 8082), appws, handler_class=WebSocketHandler).serve_forever()