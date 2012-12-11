from gevent import monkey; monkey.patch_all()
from bottle import request, response, Bottle, abort
import gevent
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketHandler, WebSocketError
from impl.test import *
from impl.device import *
from impl.auth import *
import json, base64, time

appweb = Bottle()
wslist = {} 
@appweb.route('/test/session/<sid>/screen')
def handle_screen_websocket(sid):
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    else:
        if not sid in wslist:
            wslist[sid] = []
        ret = getTestSessionInfoEx(sid)
        if not ret is None:
            wslist[sid].append({'ws':wsock, 'snaptime':''})
            deviceinfo = ret['results']['deviceinfo']
            wsock.send('snapsize:'+json.dumps(deviceinfo))
        else:
            abort(404, 'Request device is invalid.')

    while True:
        if len(wslist[sid]) == 0:
            break
        try:
            snaptime = ''
            snapdata = ''
            snaps = getTestLiveSnaps(sid)
            lenf = len(snaps)
            if lenf > 0:
                snapdata = base64.encodestring(snaps[lenf-1]['snap'])
                snaptime = snaps[lenf-1]['snaptime']

            for ws in wslist[sid]:
                try:
                    #if snaptime != ws['snaptime']:
                    ws['ws'].send('snapshot:' + snapdata)
                    #    ws['snaptime'] = snaptime
                    #else:
                    #    ws['ws'].send('nop')
                except:
                    wslist[sid].remove(ws)

            gevent.sleep(0.3)
        except WebSocketError:
            break

if __name__ == '__main__':
    print 'LiveStream Serving on 8082...'
    WSGIServer(("", 8082), appweb, handler_class=WebSocketHandler).serve_forever()
