from bottle import request, response, Bottle, abort
import gevent
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketHandler, WebSocketError
from impl.test import *
from impl.device import *
from impl.auth import *
import json, base64, time, threading

appweb = Bottle()
wslist = [] 
@appweb.route('/test/session/<sid>/screen')
def handle_screen_websocket(sid):
    print 'handle snapshot request...'
    token = '1122334455667788'
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    else:
        wslist.append(wsock)
        wsock.send('snapsize:{"width":"600px","height":"1024px"}')

    while True:
        try:
            print 'list of ws: %s' % (len(wslist))            
            snaplive = getTestSessionSnaps(token, sid)
            lenf = len(snaplive)
            msgdata = 'nop'
            if lenf > 0:
                msgdata = 'snapshot:' + base64.encodestring(snaplive[lenf-1])
            gevent.sleep(0.1)
            for i in wslist:    
                try:
                    i.send(msgdata)
                except:
                    wslist.remove(i)
        except WebSocketError:
            break

@appweb.route('/test/session/<sid>/terminal')
def handle_console_websocket(sid):
    token = '1122334455667788'
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    else:
        wsock.send('nop')

    print 'start testcase!!!'
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
    WSGIServer(("", 8082), appweb, handler_class=WebSocketHandler).serve_forever()
