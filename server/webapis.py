from bottle import request, response, Bottle, abort
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketHandler, WebSocketError
from impl.test import *
from impl.device import *
from impl.auth import *
import json, base64, time, threading

appweb = Bottle()

@appweb.route('/user/register',method='POST')
def doRegister():
    """
    URL:/user/register
    TYPE:http/POST

    register a new account to server-side

    @type appid:string
    @param appid:the id of app/domain
    @type user:string
    @param user:the userName of account
    @type pswd:string
    @param pswd:the password of account
    @type info:JSON
    @param info:the info of account  
    @rtype: JSON
    @return: ok-{'results':1}
             error-{'errors':{'code':0,'msg':(string)info}} 
    """
    content_type = request.headers.get('Content-Type')
    if not (content_type):
    #    return {'errors':{'code':500, 'msg':'Missing Content-Type'}}
    #else:
        json = request.json
        if not json is None:
            appid = json['appid']
            username = json['username']
            password = json['password']
            userinfo = json['info']
        else:
            appid = '01'
            username = 'borqsat'
            password = 'c33367701511b4f6020ec61ded352059'
            userinfo = {'email':'borqsat@gmail.com', 'contact':'+8613911312632'}
        return wrapResults(userRegister(appid,username,password,userinfo))

@appweb.route('/user/auth',method='GET')
def doAuth():
    """
    URL:/user/auth
    TYPE:http/POST

    Get access token by username and password

    @type appid:string
    @param appid:the id of app/domain
    @type user:string
    @param user:the userName of account
    @type pswd:string
    @param pswd:the password of account
    @rtype: JSON
    @return: ok-{'results':{'token':(string)value}}
             error-{'errors':{'code':0,'msg':(string)info}} 
    """
    json = request.json
    if not json is None:
        appid = json['appid']
        username = json['username']
        password = json['password']
    else:
        appid = '01'
        username = 'borqsat'
        password = 'c33367701511b4f6020ec61ded352059'           
    return wrapResults(userAuth(appid,username,password))

@appweb.route('/test/session',method='GET')
def doGetSessionList():
    """
    URL:/test/session/all
    TYPE:http/POST

    get list of all available test sessions 

    @type sid:string
    @param sid:the id of test session
    @type data:JSON
    @param data:{'token':(string)value}
    @rtype: JSON
    @return:ok-{'results':{'sid':(string)value,'planname':(string)value,'starttime':(string)value,'endtime':(string)value,'deviceinfo':(JSON){},'cases':(arrary of JSON)}}
            error-{'errors':{'code':value,'msg':(string)info}}
    """
    content_type=request.headers.get('Content-Type')
    if not (content_type):
        #return {'errors':{'code':500, 'msg':'Missing Content-Type'}}
    #else:
        json = request.json
        if not json is None:
            token = json['token']
        else:
            token = '1122334455667788'      
        return wrapResults(getTestSessionList(token))

@appweb.route('/test/caseresult/<sid>',method='GET')
def doGetSessionInfo(sid):
    """
    URL:/test/session/<sid>
    TYPE:http/POST

    Get detail of a test session by sid

    @type sid:string
    @param sid:the id of test session
    @type data:JSON
    @param data:{'token':(string)value}
    @rtype: JSON
    @return:ok-{'results':{'sid':(string)value, 'planname':(string)value,'starttime':(string)value,'endtime':(string)value,'deviceinfo':(JSON),'cases':(arrary of JSON)}}
            error-{'errors':{'code':value,'msg':(string)info}}
    """
    content_type=request.headers.get('Content-Type')
    if not (content_type):
        #return {'errors':{'code':500, 'msg':'Missing Content-Type'}}
    #else:
        json=request.json
        if not json is None:
            token=json['token']
        else:
            token='1122334455667788'       
        return wrapResults(getTestSessionInfo(token, sid))

@appweb.route('/test/caseresult/<sid>/<tid>',method='GET')
def doGetCaseResultInfo(sid, tid):
    """
    URL:/test/caseresult/<sid>/<tid>
    TYPE:http/POST

    Get detail of a test case result by sid&tid

    @type sid:string
    @param sid:the id of test session
    @type  tid: string
    @param tid: the id of case result
    @type data:JSON
    @param data:{'token':(string)value}
    @rtype: JSON
    @return:ok-{'results':{'sid':(string)value,'tid':(string)value,'casename':(string)value,'starttime':(string)value,'endtime':(string)value,'result':(string)value ['Pass'/'Fail'/'Error'],'log':(GridFsId)value,'snapshots':(arrary of GridFsId)}}
            error-{'errors':{'code':value,'msg':(string)info}}
    """
    content_type=request.headers.get('Content-Type')
    if not (content_type):
        #return {'errors':{'code':500, 'msg':'Missing Content-Type'}}
    #else:
        json=request.json
        if not json is None:
            token=json['token']     
        else:
            token='1122334455667788'
        return wrapResults(getTestCaseInfo(token, sid, tid))

@appweb.route('/test/caseresult/<sid>/<tid>/log',method='GET')
def doGetCaseResultLog(sid, tid):
    """
    URL:/test/caseresult/<sid>/<tid>/log
    TYPE:http/POST

    Get detail of a test case result by sid&tid

    @type sid:string
    @param sid:the id of test session
    @type  tid: string
    @param tid: the id of case result
    @type data:JSON
    @param data:{'token':(string)value}
    @rtype: JSON
    @return:ok-{'results':{'sid':(string)value,'tid':(string)value,'casename':(string)value,'starttime':(string)value,'endtime':(string)value,'result':(string)value ['Pass'/'Fail'/'Error'],'log':(GridFsId)value,'snapshots':(arrary of GridFsId)}}
            error-{'errors':{'code':value,'msg':(string)info}}
    """
    content_type=request.headers.get('Content-Type')
    if not (content_type):
        #return {'errors':{'code':500, 'msg':'Missing Content-Type'}}
    #else:
        json=request.json
        if not json is None:
            token=json['token']     
        else:
            token='1122334455667788'
        record_id = sid+'_'+tid
        response.set_header('Content-Type','application/x-download')
        response.set_header('Content-Disposition','attachment; filename=log_'+record_id+'.zip',True)
        return getTestCaseLog(token, sid, tid)

@appweb.route('/test/caseresult/<sid>/<tid>/snapshot',method='GET')
def doGetCaseResultSnapshots(sid, tid):
    """
    URL:/test/caseresult/<sid>/<tid>/snapshot
    TYPE:http/POST

    Get detail of a test case result by sid&tid

    @type sid:string
    @param sid:the id of test session
    @type  tid: string
    @param tid: the id of case result
    @type data:JSON
    @param data:{'token':(string)value}
    @rtype: JSON
    @return:ok-{'results':{'sid':(string)value,'tid':(string)value,'casename':(string)value,'starttime':(string)value,'endtime':(string)value,'result':(string)value ['Pass'/'Fail'/'Error'],'log':(GridFsId)value,'snapshots':(arrary of GridFsId)}}
            error-{'errors':{'code':value,'msg':(string)info}}
    """
    content_type=request.headers.get('Content-Type')
    if not (content_type):
        #return {'errors':{'code':500, 'msg':'Missing Content-Type'}}
    #else:
        json=request.json
        if not json is None:
            token=json['token']     
        else:
            token='1122334455667788'
        results = getTestCaseSnaps(token,sid,tid)
        return {'results':results}

###################Utilities####################
def wrapResults(results):
    callback = getCallback()
    if len(callback) > 0:
        return '%s(%s);'%(callback, json.dumps(results))
    else:
        return {'results':results}

def getCallback():
    callback = ''
    try:
        for key in request.params.keys():
            if key == 'callback' or key == 'jsonp' or key == 'jsonpcallback':
                callback = request.params[key]
    except:
        pass
    return callback
##########################WebApp Server APIs##########################################
#wss = {}
#wsthread = {}
@appweb.route('/test/session/<sid>/screen')
def handle_screen_websocket(sid):
    print 'handle snapshot request...'
    token = '1122334455667788'
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    else:
        wsock.send('snapsize:{"width":"600px","height":"1024px"}')
    print 'start snapshots!!!'
    while True:
        try:
            message = wsock.receive()
            snaplive = getTestSessionSnaps(token, sid)
            lenf = len(snaplive)
            msgdata = 'nop'
            if lenf > 0:
                msgdata = 'snapshot:' + base64.encodestring(snaplive[lenf-1])
            time.sleep(0.5)
            wsock.send(msgdata)
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
    WSGIServer(("", 8080), appweb, handler_class=WebSocketHandler).serve_forever()