from bottle import request, Bottle, abort
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketHandler, WebSocketError
from impl.test import *
from impl.device import *
from impl.auth import *
import time, uuid

app = Bottle()

@app.route('/test/plan',method='GET')
def doGetTestplans(pid):
    """
    URL:/test/plan
    TYPE:http/GET

    get the contents of a test plan

    @type pid:string
    @param pid:the id of plan
    @type data:JSON
    @param data:{'token':'1122334455667788'}
    @rtype: JSON
    @return: ok-{'results':[{'pid':'001122334455667788','planname':'test1','description':'android2.3.7'},{'pid':'001122334455667789','planname':'test2','description':'android4.0.4'}...]}
             error-{'errors':{'code':0,'msg':(string)info}} 
    """

@app.route('/test/plan/create',method='POST')
def doCreateTestplan():
    """
    URL:/test/plan/create
    TYPE:http/POST

    create a test plan in server-side

    @type data:JSON
    @param data:{'token':'1122334455667788','planname':'test','description':'android2.3.7','private':0} 
    @rtype: JSON
    @return: ok-{'results':{'pid':'001122334455667788'}}
             error-{'errors':{'code':0,'msg':(string)info}} 
    """

@app.route('/test/plan/<pid>',method='GET')
def doGetTestplanInfo(pid):
    """
    URL:/test/plan/<pid>
    TYPE:http/GET

    get the contents of a test plan

    @type pid:string
    @param pid:the id of plan
    @type data:JSON
    @param data:{'token':'1122334455667788'}
    @rtype: JSON
    @return: ok-{'results':{'pid':'001122334455667788','description':'android2.3.7','cases':[{'cid':'01','casename':'testMTCall'},{'cid':'02','casename':'testMOCall'}...]}}
             error-{'errors':{'code':0,'msg':(string)info}} 
    """

@app.route('/test/plan/<pid>/delete',method='POST')
def doDeleteTestplan(pid):
    """
    URL:/test/plan/<pid>/delete
    TYPE:http/POST

    delete a test plan from server-side

    @type pid:string
    @param pid:the id of plan
    @type data:JSON
    @param data:{'token':'1122334455667788'}
    @rtype: JSON
    @return: ok-{'results':1}
             error-{'errors':{'code':0,'msg':(string)info}} 
    """


@app.route('/test/plan/<pid>/addcase',method='POST')
def doAddPlanCase(pid):
    """
    URL:/test/plan/<pid>/addcase
    TYPE:http/POST

    insert several cases into test plan

    @type pid:string
    @param pid:the id of plan
    @type data:JSON
    @param data:{'token':'1122334455667788','cids':['01','02']}
    @rtype: JSON
    @return: ok-{'results':1}
             error-{'errors':{'code':0,'msg':(string)info}} 
    """

@app.route('/test/plan/<pid>/removecase',method='POST')
def doRemovePlanCase(sid):
    """
    URL:/test/plan/<pid>/removecase
    TYPE:http/POST

    remove several cases from test plan

    @type pid:string
    @param pid:the id of plan
    @type data:JSON
    @param data:{'token':'1122334455667788','cids':['01','02']}
    @rtype: JSON
    @return: ok-{'results':1}
             error-{'errors':{'code':0,'msg':(string)info}} 
    """

@app.route('/test/testcase/create',method='POST')
def doCreateCase():
    """
    URL:/test/testcase/create
    TYPE:http/POST

    create a new case in server-side

    @type info:JSON
    @param info:{'token':'1122334455667788','casename':'testMTCall','description':'MTCall'} 
    @rtype: JSON
    @return: ok-{'results':{'cid':'01'}}
             error-{'errors':{'code':0,'msg':(string)info}} 
    """

@app.route('/test/testcase/<cid>',method='GET')
def doGetCaseContent(cid):
    """
    URL:/test/testcase/<cid>
    TYPE:http/GET

    get the case content from server-side

    @type cid:string
    @param cid:the id of testcase
    @rtype: JSON/binary stream
    @return: ok- case content in file binary
             error-{'errors':{'code':0,'msg':(string)info}}
    """

@app.route('/test/testcase/<cid>/fileupload',method='PUT')
def doUploadCasefile(cid):
    """
    URL:/test/testcase/<cid>/fileupload
    TYPE:http/PUT

    upload the case content to server-side

    @type cid:string
    @param cid:the id of testcase
    @type fileData:binary stream
    @param fileData:content of file
    @rtype: JSON 
    @return: ok-{'results':1}
             error-{'errors':{'code':0,'msg':(string)info}}
    """

if __name__ == '__main__':
    WSGIServer(("", 8084), app).serve_forever()