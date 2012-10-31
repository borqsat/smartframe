from gevent import monkey; monkey.patch_all()
from bottle import request,response, Bottle, abort
from gevent.pywsgi import WSGIServer
from impl.test import *
from impl.device import *
from impl.auth import *
import time, uuid

app = Bottle()

###########################Test Server APIS##############################
@app.route('/test/session/<sid>/create',method='POST')
def doCreateSession(sid):
    """
    URL:/test/session/<sid>/create
    TYPE:http/POST

    upload a test session to server.

    @type data:JSON
    @param data:{'token':(string)value,
                'starttime':(string)timevalue,
                'planname':(string)value,
                'deviceinfo':{'deviceid':(string)value,'product':(string)value,'buildversion':(string)value,'height':(int)value,'width':(int)value}}
    @rtype: JSON
    @return:ok-{'results':1}
            error-{'errors':{'code':value,'msg':(string)info}}
    """
    content_type = request.headers.get('Content-Type')
    if not (content_type):
        return {'errors':{'code':500, 'msg':'Missing Content-Type'}}
    else:
        json = request.json
        if not json is None:
            token = json['token']  
            planname = json['planname']  
            starttime = json['starttime']
            deviceid = json['deviceid']            
            deviceinfo = json['deviceinfo'] 
        else:
            token = '1122334455667788'      
            planname = 'testplan'
            starttime = time.strftime('%Y.%m.%d-%H.%M.%S', time.localtime(time.time()))
            deviceid = '0123456789ABCDEF'
            deviceinfo = {'product':'AT390', 'revision':'6628', 'width':480, 'height':800}
        return createTestSession(token, sid, planname, starttime, deviceid, deviceinfo)

@app.route('/test/session/<sid>/update',method='POST')
def doUpdateSession(sid):
    """
    URL:/test/session/<sid>/update
    TYPE:http/POST

    upload a test session to server.

    @type data:JSON
    @param data:{'token':(string)value,
                 'endtime':(string)timevalue}
    @rtype: JSON
    @return:ok-{'results':1}
            error-{'errors':{'code':value,'msg':(string)info}}
    """
    content_type = request.headers.get('Content-Type')
    if not (content_type):
        return {'errors':{'code':500, 'msg':'Missing Content-Type'}}
    else:
        json = request.json
        if not json is None:
            token = json['token']
            endtime = json['endtime']
        else:
            token = '1122334455667788'
            endtime = 'N/A'
        return updateTestSession(token, sid, endtime)

@app.route('/test/session/<sid>/delete',method='POST')
def doDeleteSession(sid):
    """
    URL:/test/session/<sid>/delete
    TYPE:http/POST

    delete a test session from server.

    @type data:JSON
    @param data:{'token':(string)value}
    @rtype: JSON
    @return:ok-{'results':1}
            error-{'errors':{'code':value,'msg':(string)info}}
    """
    content_type = request.headers.get('Content-Type')
    if not (content_type):
        return {'errors':{'code':500, 'msg':'Missing Content-Type'}}
    else:
        json = request.json
        if not json is None:
            token = json['token']  
        else:
            token = '1122334455667788'
        return deleteTestSession(token, sid)

@app.route('/test/caseresult/<sid>/<tid>/create',method='POST')
def doCreateTestResult(sid, tid):
    """
    URL:/test/caseresult/<sid>/<tid>/create
    TYPE:http/POST
    
    Creating a test case result.

    @type sid:string
    @param sid:the id of test session
    @type  tid: string
    @param tid: the id of case result
    @type data:JSON
    @param data:{'token':(string)value,'caseName':(string)value, 'starttime':(string)timestamp}
    @rtype:JSON
    @return:ok-{'results':1}
            error-{'errors':{'code':value,'msg':(string)info}}
    """
    content_type = request.headers.get('Content-Type')
    if not (content_type):
        return {'errors':{'code':500, 'msg':'Missing Content-Type'}}
    else:
        json = request.json
        if not json is None:
            token = json['token'] 
            casename = json['casename']
            starttime = json['starttime']
        else:
            token = '1122334455667788'
            casename = 'N/A'
            starttime = time.strftime('%Y.%m.%d-%H.%M.%S', time.localtime(time.time()))
        return createCaseResult(token, sid, tid, casename, starttime)

@app.route('/test/caseresult/<sid>/<tid>/update',method='POST')
def doUpdateTestResult(sid, tid):
    """
    URL:/test/caseresult/<sid>/<tid>/update
    TYPE:http/POST

    Update the test case result by the tid of test case.

    @type sid:string
    @param sid:the id of test session
    @type  tid: string
    @param tid: the id of case result
    @type data:JSON
    @param data:{'token':(string)value,'result':value ['Pass'/'Fail'/'Error'],'time':(string)timestamp}
    @rtype:JSON
    @return:ok-{'results':1}
            error-{'errors':{'code':value,'msg':(string)info}}
    """
    content_type = request.headers.get('Content-Type')
    if not (content_type):
        return {'errors':{'code':500, 'msg':'Missing Content-Type'}}
    else:
        json = request.json
        if not json is None:
            token = json['token'] 
            status = json['result']
            traceinfo = json['traceinfo']
            endtime = json['time']
        else:
            token = '1122334455667788'
            status = 'N/A'
            traceinfo = 'N/A'
            endtime = 'N/A'
        return updateCaseResult(token, sid, tid, status, traceinfo, endtime)

@app.route('/test/caseresult/<sid>/<tid>/fileupload',method='PUT')
def doUploadFile(sid, tid):
    """
    URL:/test/caseresult/<sid>/<tid>/fileupload
    TYPE:http/PUT

    Update the test case result by the tid of test case.

    @type sid:string
    @param sid:the id of test session
    @type  tid: string
    @param tid: the id of case result
    @type data:JSON
    @param data:{'token':(string)value}
    @type fileData:binary stream
    @param fileData:content of file (logzip/snapshot)    
    @rtype:JSON
    @return:ok-{'results':1}
            error-{'errors':{'code':value,'msg':(string)info}}
    """
    content_type = request.headers.get('Content-Type')
    external_type = request.headers.get('Ext-Type')
    token = request.headers.get('token')
    if not (content_type):
        return {'errors':{'code':500, 'msg':'Missing Content-Type'}}
    elif not (token):
        return {'errors':{'code':500, 'msg':'Missing token'}}
    else:
        if content_type == 'image/png':
            ftype = 'png'
        else:
            ftype = 'zip'
        rawdata = request.body.read()
        if not (external_type):
            ctype = external_type
        else:
            ctype = ''
        return uploadCaseResultFile(token, sid, tid, rawdata, ftype, ctype)

if __name__ == '__main__':
    print 'TestServer Serving on 8081...'
    WSGIServer(("", 8081), app).serve_forever()