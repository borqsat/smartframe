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
from .plugins import LoginPlugin, ContentTypePlugin

from .. import tasks

appweb = Bottle()

contenttype_plugin = ContentTypePlugin()
appweb.install(contenttype_plugin)

login_plugin = LoginPlugin(getuserid=getUserId,
                           request_token_param="token",
                           login=True)  # login is required by default
appweb.install(login_plugin)


@appweb.hook("after_request")
def crossDomianHook():
    response.headers["Access-Control-Allow-Origin"] = "*"


@appweb.error(405)
def method_not_allowed(res):  # workaround to support cross-domain request
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
def accountBasicActionBeforeLogin():
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
    return doAccountBasicActionBeforeLogin(request.json)

@appweb.route('/user/<uid>', method='POST',content_type=['application/json','multipart/form-data'])
def accountBasicActionAfterLogin():
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
    return doAccountBasicActionAfterLogin(uid, request.json)

@appweb.route('/user/<uid>', method='GET')
def accountGetAction():
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
    return doAccountGetAction(uid, request.params)


@appweb.route('/account/active', method='POST', content_type='application/json')
def doActiveUser(uid, token):
    return "123"

@appweb.route('/group', method='POST',content_type='application/json')
def groupBasicAction():
    """
    URL:/group
    TYPE:http/POST

    create new group
    @request  'action': 'create'
              'data':{'token':(string)token, 'groupname':(string)name, 'info':(JSON)info}
    @return: ok-'data':{}

    delete group 
    @request  'action': 'delete'
              'data':{'token':(string)token, 'gid':(string)gid}
    @return: ok-'data':{}
    """
    return doGroupBasicAction(request.json)

@appweb.route('/group/<gid>/member', method='POST', content_type='application/json')
def groupMemeberAction():
    """
    URL:/group/<gid>/member
    TYPE:http/POST

    add members to a exist group
    @request  'action': 'addmember'
              'data': {'token':(string)token, 'members':[{'uid':(int)uid,'role':(int)roleId}]}
    @return: ok-'data':{}
    
    modify the role of a user in group
    @request  'action': 'setmember'
              'data': {'token':(string)token, 'members':[{'uid':(int)uid,'role':(int)roleId}]}
    @return: ok-'data':{}

    remove members from a group
    @request  'action': 'delmember'
              'data': {'token':(string)token, 'members':[{'uid':(int)uid,'role':(int)roleId}]}
    @return: ok-'data':{}
    """
    return doGroupMemeberAction(gid,request.json)

@appweb.route('/group/<gid>/info', method='GET')
def groupGetAction(gid):
    """
    URL:/group/<gid>/info
    TYPE:http/GET

    get group profile by id
    @request  'action': 'info'
              'data': {'token':(string)token}
    @return:  ok-'data':{'groupname'(string)groupname, 'members':[{'uid':(int)uid1, 'role':(int)roleId1},{'uid':(int)uid2, 'role':(int)roleId2},...]}

    get sessions summary of a group
    @request  'action': 'testsummary'
              'data': {'token':(string)token}
    @return:   ok-'data':{'count':(int)count, 'sessions':[ {planname':(string)value,'starttime':(string)value, 'result':{'total':(int)value, 'pass':(int)value, 'fail':(int)value, 'error':(int)value}, 'runtime':(string)value},... ]}
    """
    return doGroupGetAction(gid, request.json)

@appweb.route('/group/<gid>/session/<sid>', method='POST', content_type='application/json')
def testSessionBasicAction():
    """
    URL:/group/<gid>/test/<sid>
    TYPE:http/POST

    create a test session in group
    @request  'action': 'create'
              'data': {'token':(string)token,'planname':(string)value,'starttime':(string)value,'deviceinfo':{'id':(string)id,'revision':(string)revision,'product':(string)product, 'width':(int)width, 'height':(int)height}}
    @return:   ok-'data':{}

    Update the test case result by the tid of test case.
    @request  'action': 'update'
              'data': {'token':(string)token,'endtime':(string)endtime, 'status':(string)status}
    @return:   ok-'data':{}

    delete a test session from group.
    @request  'action': 'delete'
              'data': {'token':(string)token,'gid':(string)gid, 'sid':(string)sid}
    @return:   ok-'data':{}
    """
    return doTestSessionBasicAction(gid,sid,request.json)

@appweb.route('/group/<gid>/session/<sid>', method='GET')
def testSessionGetAction(gid, sid):
    """
    URL:/group/<gid>/test/<sid>
    TYPE:http/GET

    Get results of a test session by sid
    @request  'action': 'results'
              'data': {'token':(string)token,'gid':(string)gid, 'sid':(string)sid}
    @return:   ok-'data':{'count':(int)count, 'paging':{'pagesize':(int)pagesize,'totalpage':(int)totalpage,'curpage':(int)curPage },'cases':[{'casename':(string)casename, 'starttime':(string)}, 'result':(pass,fail,error), 'log':(string)logfileKey, snaps':[]...]}}

    Get summary of a test session by sid
    @request  'action': 'summary'
              'data': {'token':(string)token,'gid':(string)gid, 'sid':(string)sid}
    @return:   ok-data':{...}
    """
    return doTestSessionGetAction(gid,sid,request.json)

@appweb.route('/group/<gid>/test/<sid>/case/<tid>', method='POST', content_type='application/json')
def testCaseBasicAction():
    '''
    URL:/group/<gid>/test/<sid>/case/<tid>
    TYPE:http/POST

    Creating a test case result.
    @request  'action': 'create'
              'data': {'token':(string)value,'caseName':(string)value, 'starttime':(string)timestamp}
    @return:   ok-'data':{}

    Update the test case result by the tid of test case.
    @request  'action': 'update'
              'data': {'token':(string)value,'result':value ['Pass'/'Fail'/'Error'],'time':(string)timestamp}
    @return:   ok-'data':{}
    '''
    return doTestCaseBasicAction(gid,sid,tid,request.json)

@appweb.route('/group/<gid>/test/<sid>/case/<tid>/fileupload', method='PUT', content_type=['application/zip', 'image/png'], login=False)
def doUploadCaseFile(gid, sid, tid):
    return "123"

@appweb.route('/group/<gid>/test/<sid>/case/<tid>/snaps', method='GET')
def doGetCaseResultSnapshots(gid, sid, tid):
    return "123"


if __name__ == '__main__':
    print 'WebServer Serving on 8080...'
    WSGIServer(("", 8080), appweb).serve_forever()