from gevent import monkey; monkey.patch_all()
from bottle import request, response, Bottle, abort
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketHandler, WebSocketError
from impl.test import *
from impl.device import *
from impl.auth import *
import json, base64, time

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
    jsond = request.json
    if not jsond is None:
        appid = jsond['appid']
        username = jsond['username']
        password = jsond['password']
        info = jsond['info']
        return wrapResults(userRegister(appid,username,password,info))
    else:
        return wrapResults({"errors":{"msg":"Invalid params!", "code":"03"}})

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
    jsond = request.params
    if not jsond is None:
        appid = jsond['appid']
        username = jsond['username']
        password = jsond['password']
        return wrapResults(userAuth(appid,username,password))
    else:
        return wrapResults({"errors":{"msg":"Invalid params!", "code":"03"}})

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
    jsond = request.params
    if not jsond is None:
        token = jsond['token']
        return wrapResults(getTestSessionList(token))
    else:
        return wrapResults({"errors":{"msg":"Invalid params!", "code":"03"}})

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
    jsond = request.params
    if not jsond is None:
        token = jsond['token']
        return wrapResults(getTestSessionInfo(token, sid))
    else:
        return wrapResults({"errors":{"msg":"Invalid params!", "code":"03"}})    

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
    jsond = request.params
    if not jsond is None:
        token = jsond['token']
        return wrapResults(getTestCaseInfo(token, sid, tid))
    else:
        return wrapResults({"errors":{"msg":"Invalid params!", "code":"03"}}) 

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
    jsond = request.params
    if not jsond is None:
        token = jsond['token']
        record_id = sid+'_'+tid
        response.set_header('Content-Type','application/x-download')
        response.set_header('Content-Disposition','attachment; filename=log_'+record_id+'.zip',True)
        return getTestCaseLog(token, sid, tid)
    else:
        return wrapResults({"errors":{"msg":"Invalid params!", "code":"03"}}) 

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
    jsond = request.params
    if not jsond is None:
        token = jsond['token']
        return wrapResults(getTestCaseSnaps(token,sid,tid))
    else:
        return wrapResults({"errors":{"msg":"Invalid params!", "code":"03"}})

###################Utilities####################
def wrapResults(results):
    callback = getCallback()
    if len(callback) > 0:
        return '%s(%s);'%(callback, json.dumps(results))
    else:
        return results

def getCallback():
    callback = ''
    try:
        for key in request.params.keys():
            if key == 'callback' or key == 'jsonp' or key == 'jsonpcallback':
                callback = request.params[key]
    except:
        pass
    return callback

if __name__ == '__main__':
    print 'WebServer Serving on 8080...'
    WSGIServer(("", 8080), appweb).serve_forever()