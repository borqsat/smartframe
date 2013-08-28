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


# @appweb.route('/account/register', method='POST', content_type='application/json', login=False)
# def doRegister():
# @appweb.route('/account/forgotpasswd', method='POST', content_type='application/json', login=False)
# def doForgotpasswd():
# @appweb.route('/account/login', method='POST', content_type='application/json', login=False)
# def doLogin():

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

# @appweb.route('/account/changepasswd', method='POST', content_type='application/json')
# def doChangePassword(uid):
# @appweb.route('/account/update', method='POST', content_type=['application/json','multipart/form-data'])
# def doUpdateUserInfo(uid):
# @appweb.route('/account/invite', method='POST', content_type='application/json')
# def doInviteUser(uid):
# @appweb.route('/account/logout', method='GET')
# def doLogout(token):
@appweb.route('/user/<uid>', method='POST',content_type=['application/json','multipart/form-data'])
def doAccountWithUid():
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


# @appweb.route('/account/list', method='GET')
# def accountlist():
# @appweb.route('/account/info', method='GET')
# def doGetUserInfo(uid):
@appweb.route('/user/<uid>', method='GET')
def doGetAccountInfo():
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
    return  null


# @appweb.route('/group/create', method='POST', content_type='application/json')
# def doCreateGroup(uid):
# @appweb.route('/group/<gid>/delete', method='GET')
# def doDeleteGroup(uid, gid):
@appweb.route('/group', method='POST',content_type='application/json')
def groupAction():
    """
    URL:/group
    TYPE:http/POST

    create new group
    @type data:JSON
    @param data:{'action': 'create', 'data':{'token':(string)token, 'groupname':(string)name, 'info':(JSON)info}}
    @rtype: JSON
    @return: ok-{'results':'ok', 'data':{}, 'msg': ''}
             error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}

    delete group 
    @type data:JSON
    @param data:{'action': 'delete', 'data':{'token':(string)token, 'gid':(string)gid}}
    @rtype: JSON
    @return: ok-{'results':'ok', 'data':{}, 'msg': ''}
             error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}
    """
    return doGroupAction(request.json)

# @appweb.route('/group/<gid>/addmember', method='POST', content_type='application/json')
# def doAddmemberToGroup(gid, uid):
# @appweb.route('/group/<gid>/setmember', method='POST', content_type='application/json')
# def doSetmemberInGroup(gid, uid):
# @appweb.route('/group/<gid>/delmember', method='POST', content_type='application/json')
# def doRemovememberFromGroup(gid, uid):

@appweb.route('/group/<gid>/member', method='POST', content_type='application/json')
def doMemberToGroupAction():
    """
    URL:/group/<gid>/member
    TYPE:http/POST

    add members to a exist group
    @type data:JSON
    @param data:{'action': 'addmember', 'data': {'token':(string)token, 'members':[{'uid':(int)uid,'role':(int)roleId}]}}
    @rtype: JSON
    @return: ok-{'results':'ok', 'data':{}, 'msg': ''}
             error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}
    
    modify the role of a user in group
    @type data:JSON
    @param data:{'action': 'setmember', 'data': {'token':(string)token, 'members':[{'uid':(int)uid,'role':(int)roleId}]}}
    @rtype: JSON
    @return: ok-{'results':'ok', 'data':{}, 'msg': ''}
             error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}

    remove members from a group
    @type data:JSON
    @param data: {'action': 'delmember', 'data': {'token':(string)token, 'members':[{'uid':(int)uid,'role':(int)roleId}]}}
    @rtype: JSON
    @return: ok-{'results':'ok', 'data':{}, 'msg': ''}
             error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}
    """
	return memberToGroupAction(gid,request.json)

# @appweb.route('/group/<gid>/info', method='GET')
# def doGetGroupInfo(gid, uid):
# @appweb.route('/group/<gid>/testsummary', method='GET')
# def doGetGroupTestSessions(gid):

@appweb.route('/group/<gid>/info', method='GET')
def groupInfo(gid):
    """
    URL:/group/<gid>/info
    TYPE:http/GET

    get group profile by id
    @type data:JSON
    @param data: {'action': 'info', 'data': {'token':(string)token}}
    @rtype: JSON
    @return: ok-{'results':'ok', 'data':{'groupname'(string)groupname, 'members':[{'uid':(int)uid1, 'role':(int)roleId1},{'uid':(int)uid2, 'role':(int)roleId2},...]}, 'msg': ''}
             error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}

    get sessions summary of a group
    @type data:JSON
    @param data: {'action': 'testsummary', 'data': {'token':(string)token}}
    @rtype: JSON
    @return: ok-{'results':'ok', 'data':{'count':(int)count, 'sessions':[ {planname':(string)value,'starttime':(string)value, 'result':{'total':(int)value, 'pass':(int)value, 'fail':(int)value, 'error':(int)value}, 'runtime':(string)value},... ] }}
             error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}
    """
	return groupInfo(gid, request.json)

# @appweb.route('/group/<gid>/test/<sid>/create', method='POST', content_type='application/json')
# def doCreateGroupTestSession(gid, sid, uid):
# @appweb.route('/group/<gid>/test/<sid>/update', method='POST', content_type='application/json')
# def doUpdateGroupTestSession(gid, sid):
# @appweb.route('/group/<gid>/test/<sid>/delete', method='GET')
# def doDeleteGroupTestSession(uid, gid, sid):

@appweb.route('/group/<gid>/session/<sid>', method='POST', content_type='application/json')
def doTestSessionAction():
    """
    URL:/group/<gid>/test/<sid>
    TYPE:http/POST

    create a test session in group
    @type data:JSON
    @param data:{'action': 'create', 'data': {'token':(string)token,'planname':(string)value,'starttime':(string)value,'deviceinfo':{'id':(string)id,'revision':(string)revision,'product':(string)product, 'width':(int)width, 'height':(int)height}}}
    @rtype:JSON
    @return: ok-{'results':'ok', 'data':{}, 'msg': ''}
             error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}

    Update the test case result by the tid of test case.
    @type data:JSON
    @param data:{'action': 'update', 'data': {'token':(string)token,'endtime':(string)endtime, 'status':(string)status}}
    @rtype:JSON
    @return: ok-{'results':'ok', 'data':{}, 'msg': ''}
             error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}

    delete a test session from group.
    @type data:JSON
    @param data:{'action': 'delete', 'data': {'token':(string)token,'gid':(string)gid, 'sid':(string)sid}}
    @rtype: JSON
    @return: ok-{'results':'ok', 'data':{}, 'msg': ''}
             error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}

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

    Get results of a test session by sid
    @type data:JSON
    @param data:{'action': 'results', 'data': {'token':(string)token,'gid':(string)gid, 'sid':(string)sid}}
    @rtype: JSON
    @return:ok-{'results':'ok', 'data':{'count':(int)count, 'paging':{'pagesize':(int)pagesize,'totalpage':(int)totalpage,'curpage':(int)curPage },'cases':[{'casename':(string)casename, 'starttime':(string)}, 'result':(pass,fail,error), 'log':(string)logfileKey, snaps':[]...]}}, 'msg': ''}
            error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}

    Get summary of a test session by sid
    @type data:JSON
    @param data:{'action': 'summary', 'data': {'token':(string)token,'gid':(string)gid, 'sid':(string)sid}}
    @rtype: JSON
    @return:ok-{'results':'ok', 'data':{...}, 'msg': ''}
            error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}

    ....
    """
	return getSessionAction(gid,sid,request.json)

# @appweb.route('/group/<gid>/test/<sid>/case/<tid>/create', method='POST', content_type='application/json')
# def doCreateCaseResult(gid, sid, tid):
# @appweb.route('/group/<gid>/test/<sid>/case/<tid>/update', method='POST', content_type='application/json')
# def doUpdateCaseResult(gid, sid, tid):

@appweb.route('/group/<gid>/test/<sid>/case/<tid>', method='POST', content_type='application/json')
def doCaseResultAction():
    '''
    URL:/group/<gid>/test/<sid>/case/<tid>
    TYPE:http/POST

    Creating a test case result.
    @type data:JSON
    @param data:{'action': 'create', 'data': {'token':(string)value,'caseName':(string)value, 'starttime':(string)timestamp}}
    @rtype:JSON
    @return:ok-{'results':'ok', 'data':{}, 'msg': ''}
            error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}

    Update the test case result by the tid of test case.
    @type data:JSON
    @param data:{'action': 'update', 'data': {'token':(string)value,'result':value ['Pass'/'Fail'/'Error'],'time':(string)timestamp}}
    @rtype:JSON
    @return:ok-{'results':'ok', 'data':{}, 'msg': ''}
            error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}
    '''
	return caseResultAction(gid,sid,tid,request.json)


@appweb.route('/group/<gid>/test/<sid>/case/<tid>/fileupload', method='PUT', content_type=['application/zip', 'image/png'], login=False)
def doUploadCaseFile(gid, sid, tid):
    return null

@appweb.route('/group/<gid>/test/<sid>/case/<tid>/snaps', method='GET')
def doGetCaseResultSnapshots(gid, sid, tid):
    return null


if __name__ == '__main__':
    print 'WebServer Serving on 8080...'
    WSGIServer(("", 8080), appweb).serve_forever()