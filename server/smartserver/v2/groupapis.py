#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

from bottle import request, response, Bottle, HTTPResponse
from gevent.pywsgi import WSGIServer

from .impl.test import *
from .impl.account import *
from .impl.group import *
from .sendmail import *

appweb = Bottle()
"""
contenttype_plugin = ContentTypePlugin()
appweb.install(contenttype_plugin)

login_plugin = LoginPlugin(getuserid=getUserId,
                           request_token_param="token",
                           login=True)  # login is required by default
appweb.install(login_plugin)
"""

@appweb.hook("after_request")
def crossDomianHook():
    response.headers["Access-Control-Allow-Origin"] = "*"

@appweb.error(405)
def method_not_allowed(res):
    if request.method == 'OPTIONS':
        new_res = HTTPResponse()
        new_res.set_header('Access-Control-Allow-Origin', '*')
        new_res.headers[
            "Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE"
        if request.headers.get("Access-Control-Request-Headers"):
            new_res.headers["Access-Control-Allow-Headers"] = request.headers[
                "Access-Control-Request-Headers"]
        return new_res
    res.headers['Allow'] += ', OPTIONS'
    return request.app.default_error_handler(res)


@appweb.route('/account', method='POST', content_type='application/json', login=False)
def doAccountWithOutUid():
    """
    URL:/account
    TYPE:http/POST
    @type data:JSON
    @param data:{'subc': '', 'data':{}}
    @rtype: JSON
    @return: ok-{'results':'ok', 'data':{}, 'msg': ''}
             error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}
    ---------------------------------------------------------------------------------------
    |support|subc          |data
    |       |register      |{'username':(string)username, 'password':(string)password, 'appid':(string)appid,'info':{'email':(string), 'telephone':(string)telephone, 'company':(string)company}
    |       |forgotpasswd  |{'email':(string)mailaddress}
    |       |login         |{'appid':(int)appid, 'username':(string)username, 'password':(string)password}
    ---------------------------------------------------------------------------------------
    """
    return accountWithOutUid(request.json)

@appweb.route('/user/<uid>', method='POST',content_type=['application/json','multipart/form-data'])
def doAccountWithUid(uid):
    """
    URL:/user/<uid>
    TYPE:http/POST
    @type data:JSON
    @param data:{'subc': '', 'data':{}}
    @rtype: JSON
    @return: ok-{'results':'ok', 'data':{}, 'msg': ''}
             error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}
    ----------------------------------------------------------------------------------------
    |support|subc          |data
    |       |changepasswd  |{'token':(string)token,'oldpassword':(string)oldpassword, 'newpassword':(string)newpassword }
    |       |update        |{'token':(string)token,'info':{'email':(string), 'telephone':(string)telephone, 'company':(string)company}}
    |       |invite        |{'token':(string)token, 'email':(string)email}
    |       |logout        |{'token':(string)token}
    -----------------------------------------------------------------------------------------
    """
    return accountWithUid(uid, request.json)

@appweb.route('/user/<uid>', method='GET')
def doGetAccountInfo(uid):
    """
    URL:/account
    TYPE:http/GET
    @type data:JSON
    @param data:{'subc': '', 'data':{}}
    @rtype: JSON
    @return: ok-{'results':'ok', 'data':{}, 'msg': ''}
             error-{'results':'error', 'data':{}, 'msg': '(string)info'}
    ----------------------------------------------------------------------------------------
    |support|subc          |data  |return data 
    |       |list          |null  |{'count':(int)value, 'users':[{'uid':(string)uid,'username':(string)username},{'uid':(string)uid,'username':(string)username}]}}
    |       |info          |null  |{'username':(string)username,'inGroups':[{'gid':gid1,'groupname':(string)name1},{'gid':gid2,'groupname':(string)name2},...],'info':{'email':(string)email, 'telephone':(string)telephone, 'company':(string)company}}
    -----------------------------------------------------------------------------------------
    """
    return getAccountInfo(uid)

@appweb.route('/account/active', method='POST', content_type='application/json')
def doActiveUser(uid, token):
    return null

@appweb.route('/group', method='POST',content_type='application/json')
def groupAction():
    """
    URL:/group
    TYPE:http/POST
    @type data:JSON
    @param data:{'subc': '', 'data':{}}
    @rtype: JSON
    @return: ok-{'results':'ok', 'data':{}, 'msg': ''}
             error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}
    ----------------------------------------------------------------------------------------
    |support|subc          |data 
    |       |create        |{token':(string)token, 'groupname':(string)name, 'info':(JSON)info}'}  
    |       |delete        |{'token':(string)token, 'gid':(string)gid}
    -----------------------------------------------------------------------------------------
    """
    return doGroupAction(request.json)

@appweb.route('/group/<gid>/member', method='POST', content_type='application/json')
def doMemberToGroupAction(gid):
    """
    URL:/group/<gid>/member
    TYPE:http/POST
    @type data:JSON
    @param data:{'subc': '', 'data':{}}
    @rtype: JSON
    @return: ok-{'results':'ok', 'data':{}, 'msg': ''}
             error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}
    ----------------------------------------------------------------------------------------
    |support|subc          |data 
    |       |addmember     |{'token':(string)token, 'members':[{'uid':(int)uid,'role':(int)roleId}]}  
    |       |setmember     |{'token':(string)token, 'members':[{'uid':(int)uid,'role':(int)roleId}]}
    |       |delmember     |{'token':(string)token, 'members':[{'uid':(int)uid,'role':(int)roleId}]}
    -----------------------------------------------------------------------------------------
    """
    return memberToGroupAction(gid,request.json)

@appweb.route('/group/<gid>/info', method='GET')
def groupInfo(gid):
    """
    URL:/group/<gid>/info
    TYPE:http/GET
    @type data:JSON
    @param data:{'subc': '', 'data':{}}
    @rtype: JSON
    @return: ok-{'results':'ok', 'data':{}, 'msg': ''}
             error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}
    ----------------------------------------------------------------------------------------
    |support|subc          |data                   |return data
    |       |info          |{'token':(string)token,|{'groupname'(string)groupname, 'members':[{'uid':(int)uid1, 'role':(int)roleId1},{'uid':(int)uid2, 'role':(int)roleId2},...]} 
    |       |testsummary   |{'token':(string)token,|{'count':(int)count, 'sessions':[ {planname':(string)value,'starttime':(string)value, 'result':{'total':(int)value, 'pass':(int)value, 'fail':(int)value, 'error':(int)value}, 'runtime':(string)value},... ] }}
    -----------------------------------------------------------------------------------------
    """
    return groupInfo(gid, request.json)

@appweb.route('/group/<gid>/session/<sid>', method='POST', content_type='application/json')
def doTestSessionAction(gid,sid):
    """
    URL:/group/<gid>/test/<sid>
    TYPE:http/POST
    @type data:JSON
    @param data:{'subc': '', 'data':{}}
    @rtype: JSON
    @return: ok-{'results':'ok', 'data':{}, 'msg': ''}
             error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}
    ----------------------------------------------------------------------------------------
    |support|subc   |data                   
    |       |create |{'token':(string)token,'planname':(string)value,'starttime':(string)value,'deviceinfo':{'id':(string)id,'revision':(string)revision,'product':(string)product, 'width':(int)width, 'height':(int)height}}
    |       |update |{'token':(string)token,'endtime':(string)endtime, 'status':(string)status}
    |       |delete |{'token':(string)token,'gid':(string)gid, 'sid':(string)sid}
    -----------------------------------------------------------------------------------------
    """
    return testSessionAction(gid,sid,request.json)

# @appweb.route('/group/<gid>/test/<sid>/results', method='GET')
# def doGetSessionInfo(gid, sid):   
# @appweb.route('/group/<gid>/test/<sid>/live', method='GET')
# def getSessionLiveData(gid, sid):
# @appweb.route('/group/<gid>/test/<sid>/poll', method='GET')
# def checkSessionUpdated(gid, sid):
# @appweb.route('/group/<gid>/test/<sid>/history', method='GET')
# def getSessionHistoryData(gid, sid):
# @appweb.route('/group/<gid>/test/<sid>/summary', method='GET')
# def doGetSessionSummary(gid, sid):

@appweb.route('/group/<gid>/session/<sid>', method='GET')
def doGetSessionAction(gid, sid):
    """
    URL:/group/<gid>/test/<sid>
    TYPE:http/GET
    @type data:JSON
    @param data:{'subc': '', 'data':{}}
    @rtype: JSON
    @return: ok-{'results':'ok', 'data':{}, 'msg': ''}
             error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}
    ----------------------------------------------------------------------------------------
    |support|subc    |data                                                          |return data
    |       |results |{'token':(string)token,'gid':(string)gid, 'sid':(string)sid}} |:{'count':(int)count, 'paging':{'pagesize':(int)pagesize,'totalpage':(int)totalpage,'curpage':(int)curPage },'cases':[{'casename':(string)casename, 'starttime':(string)}, 'result':(pass,fail,error), 'log':(string)logfileKey, snaps':[]...]}}, 'msg': ''}
    |       |summary |{'token':(string)token,'gid':(string)gid, 'sid':(string)sid}  |
    -----------------------------------------------------------------------------------------
    """
    return getSessionAction(gid,sid,request.json)

# @appweb.route('/group/<gid>/test/<sid>/case/<tid>/create', method='POST', content_type='application/json')
# def doCreateCaseResult(gid, sid, tid):
# @appweb.route('/group/<gid>/test/<sid>/case/<tid>/update', method='POST', content_type='application/json')
# def doUpdateCaseResult(gid, sid, tid):

@appweb.route('/group/<gid>/test/<sid>/case/<tid>', method='POST', content_type='application/json')
def doCaseResultAction(gid,sid,tid):
    """
    URL:/group/<gid>/test/<sid>/case/<tid>
    TYPE:http/POST
    @type data:JSON
    @param data:{'subc': '', 'data':{}}
    @rtype: JSON
    @return: ok-{'results':'ok', 'data':{}, 'msg': ''}
             error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}
    ----------------------------------------------------------------------------------------
    |support|subc    |data                                                          
    |       |create  |{'token':(string)value,'caseName':(string)value, 'starttime':(string)timestamp}
    |       |update  |{'token':(string)value,'result':value ['Pass'/'Fail'/'Error'],'time':(string)timestamp}
    -----------------------------------------------------------------------------------------
    """
    return caseResultAction(gid,sid,tid,request.json)

@appweb.route('/group/<gid>/test/<sid>/case/<tid>/fileupload', method='PUT', content_type=['application/zip', 'image/png'], login=False)
def doUploadCaseFile(gid, sid, tid):
    return None

@appweb.route('/group/<gid>/test/<sid>/case/<tid>/snaps', method='GET')
def doGetCaseResultSnapshots(gid, sid, tid):
    return getTestCaseSnaps(gid, sid, tid)


if __name__ == '__main__':
    print 'WebServer Serving on 8080...'
    WSGIServer(("", 8080), appweb).serve_forever()
