from gevent import monkey; monkey.patch_all()
from bottle import request, response, Bottle, abort
from gevent.pywsgi import WSGIServer
from impl.test import *
from impl.account import *
from impl.group import *
import json, base64, time
import smtplib

appweb = Bottle()

def sendVerifyMail(receiver,user,token):
    sender   = 'borqsat@borqs.com'  
    subject  = 'Please active your account from SmartAT'
    mailuser = 'borqsat@borqs.com'
    mailpass = '!QAZ2wsx3edc'
      
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, receiver, subject))
    msg = msg+'Hi:\r\n'
    msg = msg+'\r\nThis mail send from smartServer automatically, do not reply this mail directly.\r\n'
    msg = msg+'\r\nYour account \"%s\" has been initialized.\r\n' % (user)
    msg = msg+'\r\nPlease verify your current email via the url as below.\r\n'    
    msg = msg+'\r\nsmart Server: http://192.168.5.216/smartserver/verify.html?token=%s\r\n' % (token)
    msg = msg+'\r\nBest Regards!\r\n'
    msg = msg+'smartServer Admin\r\n'

    smtp = None
    try:
        smtp = smtplib.SMTP_SSL()  
        smtp.connect('smtp.bizmail.yahoo.com')
        smtp.login(mailuser, mailpass)  
        smtp.sendmail(sender, receiver, msg)       
    except Exception, e:
        print e
    smtp.quit()

def sendInviteMail(receiver, user, group, token):
    sender   = 'borqsat@borqs.com'  
    subject  = 'Please active your account from SmartAT'
    mailuser = 'borqsat@borqs.com'
    mailpass = '!QAZ2wsx3edc'
      
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, receiver, subject))
    msg = msg+'Hi:\r\n'
    msg = msg+'\r\nThis mail send from smartServer automatically, do not reply this mail directly.\r\n'
    msg = msg+'\r\nYour friend \"%s\" invite you to join group [%s].\r\n' % (user, group)
    msg = msg+'\r\nYou are welcome to signup your own account via the url below.\r\n'    
    msg = msg+'\r\nsmart Server: http://ats.borqs.com/smartserver/login.html?token=%s\r\n' % (token)
    msg = msg+'\r\nBest Regards!\r\n'
    msg = msg+'smartServer Admin\r\n'

    smtp = None
    try:
        smtp = smtplib.SMTP_SSL()  
        smtp.connect('smtp.bizmail.yahoo.com')
        smtp.login(mailuser, mailpass)  
        smtp.sendmail(sender, receiver, msg)       
    except Exception, e:
        print e
    smtp.quit()

@appweb.route('/account/register',method='POST')
def doRegister():
    """
    URL:/account/register
    TYPE:http/POST

    register a new account to server-side

    @type data:JSON
    @param data:{'username':(string)username, 'password':(string)password, 'appid':(string)appid,'info':{'email':(string), 'telephone':(string)telephone, 'company':(string)company}}
    @rtype: JSON
    @return: ok-{'results':1}
             error-{'errors':{'code':(string)code,'msg':(string)info}} 
    """
    content_type = request.headers.get('Content-Type')
    if not (content_type):
        return {'errors':{'code':'500', 'msg':'Missing Content-Type'}}
    else:
        jsond = request.json
        if not jsond is None:
            appid = jsond['appid']
            username = jsond['username']
            password = jsond['password']
            info = jsond['info']
            ret = userRegister(appid, username, password, info)
            if ret.has_key('results'):
                sendVerifyMail(info['email'],username,ret['results']['token'])
            return ret
        else:
            return {'errors':{'msg':'Invalid params!', 'code':'03'}}

@appweb.route('/account/changepasswd',method='POST')
def doChangePassword():
    """
    URL:/account/change_password
    TYPE:http/POST

    update the info of user

    @type data:JSON
    @param data:{'token':(string)token,'oldpassword':(string)oldpassword, 'newpassword':(string)newpassword } 
    @rtype: JSON
    @return: ok-{'results':1}
             error-{'errors':{'code':(string)code,'msg':(string)info}} 
    """
    content_type = request.headers.get('Content-Type')
    if not (content_type):
        return {'errors':{'code':'500', 'msg':'Missing Content-Type'}}
    else:
        jsond = request.json
        if not jsond is None:
            token = jsond['token']
            oldpassword = jsond['oldpassword']
            newpassword = jsond['newpassword']
            uid = getUserId(token)
            if uid is None:
                return {'errors':{'code':'01','msg':'Invalid token.'}}
            return userChangePassword(uid,oldpassword,newpassword)
        else:
            return {'errors':{'msg':'Invalid params!', 'code':'03'}}

@appweb.route('/account/update',method='POST')
def doUpdateUserInfo():
    """
    URL:/account/update
    TYPE:http/POST

    update the info of user

    @type uid:string
    @param uid:the id of user
    @type data:JSON
    @param data:{'token':(string)token,'info':{'email':(string), 'telephone':(string)telephone, 'company':(string)company}}  
    @rtype: JSON
    @return: ok-{'results':1}
             error-{'errors':{'code':(string)code,'msg':(string)info}} 
    """
    content_type = request.headers.get('Content-Type')
    if not (content_type):
        return {'errors':{'code':'500', 'msg':'Missing Content-Type'}}
    else:
        jsond = request.json
        if not jsond is None:
            token = jsond['token']
            info = jsond['info']
            if uid is None:
                return {'errors':{'code':'01','msg':'Invalid token.'}}
            return userUpdateInfo(uid,info)
        else:
            return {'errors':{'msg':'Invalid params!', 'code':'03'}}

@appweb.route('/account/invite',method='POST')
def doInviteUser():
    """
    URL:/account/invite
    TYPE:http/POST

    Get information of user

    @type data:JSON
    @param data:{'token':(string)token, 'gid':(string)gid, 'email':(string)email}
    @rtype: JSON
    @return: ok-{'results':{'token':(string)token}}
             error-{'errors':{'code':(string)code,'msg':(string)info}}
    """
    content_type = request.headers.get('Content-Type')
    if not (content_type):
        return {'errors':{'code':'500', 'msg':'Missing Content-Type'}}
    else:
        jsond = request.json
        if not jsond is None:
            appid = jsond['appid']            
            token = jsond['token']
            email = jsond['email']
            username = jsond['username']
            groupname = jsond['groupname']            
            gid = jsond['gid']
            uid = getUserId(token)
            if uid is None:
                return {'errors':{'code':'01','msg':'Invalid token.'}}
            rdata = inviteUser(appid,email,gid,uid)
            if rdata.has_key('results'):
                sendInviteMail(email, username, groupname, ret['results']['token'])
            return rdata
        else:
            return {'errors':{'msg':'Invalid params!', 'code':'03'}}

@appweb.route('/account/active',method='POST')
def doActiveUser():
    """
    URL:/account/active
    TYPE:http/POST

    Get information of user

    @type data:JSON
    @param data:{'token':(string)token}
    @rtype: JSON
    @return: ok-{'results':{'uid':(string)uid}}
             error-{'errors':{'code':(string)code,'msg':(string)info}}
    """
    content_type = request.headers.get('Content-Type')
    if not (content_type):
        return {'errors':{'code':'500', 'msg':'Missing Content-Type'}}
    else:
        jsond = request.json
        if not jsond is None:
            token = jsond['token']
            uid = getUserId(token)
            if uid is None:
                return {'errors':{'code':'01','msg':'Invalid token.'}}
            rdata = activeUser(uid)
            userLogout(token)
            return rdata
        else:
            return {'errors':{'msg':'Invalid params!', 'code':'03'}}

@appweb.route('/account/info',method='GET')
def doGetUserInfo():
    """
    URL:/account/info
    TYPE:http/GET

    Get information of user

    @type uid:string
    @param uid:the id of user
    @type token:string
    @param token: the access token 
    @rtype: JSON
    @return: ok-{'results':{'username':(string)username,'inGroups':[{'gid':gid1,'groupname':(string)name1},{'gid':gid2,'groupname':(string)name2},...],'info':{'email':(string)email, 'telephone':(string)telephone, 'company':(string)company}}}
             error-{'errors':{'code':(string)code,'msg':(string)info}} 
    """
    jsond = request.params
    if not jsond is None:
        token = jsond['token']
        uid = getUserId(token)
        if uid is None:
            return {'errors':{'code':'01','msg':'Invalid token.'}}
        return getUserInfo(uid)
    else:
        return {'errors':{'msg':'Invalid params!', 'code':'03'}}

@appweb.route('/account/login',method='POST')
def doLogin():
    """
    URL:/account/login
    TYPE:http/POST

    Get access token by username and password
 
    @type data:JSON
    @param data:{'appid':(int)appid, 'username':(string)username, 'password':(string)password}
    @rtype: JSON
    @return: ok-{'results':{'token':(string)value}}
             error-{'errors':{'code':(string)code,'msg':(string)info}} 
    """
    content_type = request.headers.get('Content-Type')
    if not (content_type):
        return {'errors':{'msg':'Missing Content-Type','code':'500'}}
    else:
        jsond = request.json
        if not jsond is None:
            appid = jsond['appid']
            username = jsond['username']
            password = jsond['password']
            return userLogin(appid,username,password)
        else:
            return {'errors':{'msg':'Invalid params!','code':'03'}}

@appweb.route('/account/logout',method='GET')
def doLogout():
    """
    URL:/account/logout
    TYPE:http/GET

    Get access token by username and password

    @type token:string
    @param token:access token of account
    @rtype: JSON
    @return: ok-{'results':1}
             error-{'errors':{'code':(string)code,'msg':(string)info}} 
    """
    jsond = request.params
    if not jsond is None:
        token = jsond['token']
        return userLogout(token)
    else:
        return {'errors':{'msg':'Invalid params!', 'code':'03'}}

@appweb.route('/account/list',method='GET')
def doLogin():
    """
    URL:/account/list
    TYPE:http/GET

    Get access token by username and password
 
    @type data:JSON
    @param data:{'token':(string)token}
    @rtype: JSON
    @return: ok-{'results':{'count':(int)value, 'users':[{'uid':(string)uid,'username':(string)username},{'uid':(string)uid,'username':(string)username}]}}
             error-{'errors':{'code':(string)code,'msg':(string)info}} 
    """
    jsond = request.params
    if not jsond is None:
        token = jsond['token']
        uid = getUserId(token)
        if uid is None:
            return {'errors':{'code':'01','msg':'Invalid token.'}} 
        return getUserList()
    else:
        return {'errors':{'msg':'Invalid params!', 'code':'03'}}

@appweb.route('/group/create',method='POST')
def doCreateGroup():
    """
    URL:/group/create
    TYPE:http/POST

    create a new group

    @type data:JSON
    @param data:the info of account {'token':(string)token, 'groupname':(string)name, 'info':(JSON)info} 
    @rtype: JSON
    @return: ok-{'results':1}
             error-{'errors':{'code':(string)code,'msg':(string)info}} 
    """
    content_type = request.headers.get('Content-Type')
    if not (content_type):
        return {'errors':{'msg':'Missing Content-Type','code':'500'}}
    else:
        jsond = request.json
        if not jsond is None:
            token = jsond['token']
            groupname = jsond['groupname']
            info = jsond['info']
            uid = getUserId(token)
            if uid is None:
                return {'errors':{'code':'01','msg':'Invalid token.'}}      
            return createGroup(uid,groupname,info)
        else:
            return {'errors':{'msg':'Invalid params!','code':'03'}}

@appweb.route('/group/<gid>/addmember',method='POST')
def doAddmemberToGroup(gid):
    """
    URL:/group/<gid>/addmember
    TYPE:http/POST

    add members to a exist group

    @type gid:string
    @param gid:the id of Group
    @type data:JSON
    @param data:info of member list {'token':(string)token, 'members':[(int)uid1,(int)uid2,(int)uid3 ...]} 
    @rtype: JSON
    @return: ok-{'results':1}
             error-{'errors':{'code':(string)code,'msg':(string)info}} 
    """
    content_type = request.headers.get('Content-Type')
    if not (content_type):
        return {'errors':{'msg':'Missing Content-Type','code':'500'}}
    else:
        jsond = request.json
        if not jsond is None:
            token = jsond['token'] 
            members = jsond['members']
            uid = getUserId(token)
            if uid is None:
                return {'errors':{'code':'01','msg':'Invalid token.'}}
            return addGroupMembers(uid,gid,members)
        else:
            return {'errors':{'msg':'Invalid params!','code':'03'}}

@appweb.route('/group/<gid>/setmember',method='POST')
def doSetmemberInGroup(gid):
    """
    URL:/group/<gid>/setmember
    TYPE:http/POST

    modify the role of a user in group

    @type gid:string
    @param gid:the id of Group
    @type data:JSON
    @param data:info of member list {'token':(string)token, 'members':[{'uid':(int)uid,'role':(int)roleId}, {'uid':(int)uid, 'role':(int)roleId}, ...]} 
    @rtype: JSON
    @return: ok-{'results':1}
             error-{'errors':{'code':(string)code,'msg':(string)info}} 
    """
    content_type = request.headers.get('Content-Type')
    if not (content_type):
        return {'errors':{'msg':'Missing Content-Type','code':'500'}}
    else:
        jsond = request.json
        if not jsond is None:
            token = jsond['token'] 
            members = jsond['members']
            uid = getUserId(token)
            if uid is None:
                return {'errors':{'code':'01','msg':'Invalid token.'}}
            return setGroupMembers(uid,gid,members)
        else:
            return {'errors':{'msg':'Invalid params!','code':'03'}}

@appweb.route('/group/<gid>/delmember',method='POST')
def doRemovememberFromGroup(gid):
    """
    URL:/group/<gid>/delmember
    TYPE:http/POST

    remove members from a group

    @type gid:string
    @param gid:the id of Group
    @type data:JSON
    @param data: member list {'token':(string)token, 'members':[(int)uid1, (int)uid2, (int)uid3 ...]} 
    @rtype: JSON
    @return: ok-{'results':1}
             error-{'errors':{'code':(string)code,'msg':(string)info}} 
    """
    content_type = request.headers.get('Content-Type')
    if not (content_type):
        return {'errors':{'msg':'Missing Content-Type','code':'500'}}
    else:
        jsond = request.json
        if not jsond is None:
            token = jsond['token'] 
            members = jsond['members']
            uid = getUserId(token)
            if uid is None:
                return {'errors':{'code':'01','msg':'Invalid token.'}}
            return delGroupMembers(uid,gid,members)
        else:
            return {'errors':{'msg':'Invalid params!','code':'03'}}

@appweb.route('/group/<gid>/info',method='GET')
def doGetGroupInfo(gid):
    """
    URL:/group/<gid>/info
    TYPE:http/GET

    get group profile by id

    @type gid:string
    @param gid:the id of Group
    @type token:string
    @param token:access token of account 
    @rtype: JSON
    @return: ok-{'results':{'groupname'(string)groupname, 'members':[{'uid':(int)uid1, 'role':(int)roleId1},{'uid':(int)uid2, 'role':(int)roleId2},...]}}
             error-{'errors':{'code':(string)code,'msg':(string)info}} 
    """
    jsond = request.params
    if not jsond is None:
        token = jsond['token']
        uid = getUserId(token)
        if uid is None:
            return {'errors':{'code':'01','msg':'Invalid token.'}}
        return getGroupInfo(uid, gid)
    else:
        return {'errors':{'msg':'Invalid params!', 'code':'03'}}

@appweb.route('/group/<gid>/test/<sid>/create',method='POST')
def doCreateGroupTestSession(gid, sid):
    """
    URL:/group/<gid>/test/<sid>/create
    TYPE:http/POST

    create a test session in group

    @type gid:string
    @param gid:the id of Group
    @type sid:string
    @param sid:the id of testsession
    @type data:JSON
    @param data:{'token':(string)token,'planname':(string)value,'starttime':(string)value,'deviceinfo':{'id':(string)id,'revision':(string)revision,'product':(string)product, 'width':(int)width, 'height':(int)height}}
    @rtype:JSON
    @return:ok-{'results':1}
            error-{'errors':{'code':value,'msg':(string)info}}
    """
    content_type = request.headers.get('Content-Type')
    if not (content_type):
        return {'errors':{'msg':'Missing Content-Type','code':'500'}}
    else:
        json = request.json
        if not json is None:
            token = json['token']
            planname = json['planname']  
            starttime = json['starttime']
            deviceid = json['deviceid']
            deviceinfo = json['deviceinfo']
            uid = getUserId(token)
            if uid is None:
                return {'errors':{'code':'01','msg':'Invalid token.'}}
            return createTestSession(gid, uid, sid, planname, starttime, deviceid, deviceinfo)
        else:
            return {'errors':{'msg':'Invalid params!','code':'03'}}

@appweb.route('/group/<gid>/test/<sid>/case/<tid>/create',method='POST')
def doCreateCaseResult(gid, sid, tid):
    """
    URL:/group/<gid>/test/<sid>/case/<tid>/create
    TYPE:http/POST
    
    Creating a test case result.

    @type gid:string
    @param gid:the id of Group
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
            uid = getUserId(token)
            if uid is None:
                return {'errors':{'code':'01','msg':'Invalid token.'}}
            return createCaseResult(gid, sid, tid, casename, starttime)
        else:
            return {'errors':{'msg':'Invalid params!','code':'03'}}

@appweb.route('/group/<gid>/test/<sid>/case/<tid>/update',method='POST')
def doUpdateCaseResult(gid, sid, tid):
    """
    URL:/group/<gid>/test/<sid>/case/<tid>/update
    TYPE:http/POST

    Update the test case result by the tid of test case.

    @type gid:string
    @param gid:the id of Group
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
            uid = getUserId(token)
            if uid is None:
                return {'errors':{'code':'01','msg':'Invalid token.'}}
            return updateCaseResult(gid, sid, tid, status, traceinfo, endtime)
        else:
            return {'errors':{'msg':'Invalid params!','code':'03'}}            

@appweb.route('/group/<gid>/test/<sid>/case/<tid>/fileupload',method='PUT')
def doUploadCaseFile(gid, sid, tid):
    """
    URL:/group/<gid>/test/<sid>/case/<tid>/fileupload
    TYPE:http/PUT

    Update the test case result by the tid of test case.

    @type gid:string
    @param gid:the id of Group
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
    ext_type = request.headers.get('Ext-Type')
    token = request.headers.get('token')
    if not (token):
        return {'errors':{'code':500, 'msg':'Missing token'}}

    if not (content_type):
        return {'errors':{'code':500, 'msg':'Missing Content-Type'}}

    if content_type == 'image/png':
        ftype = 'png'
    else:
        ftype = 'zip'
    filedata = request.body.read()
    if not ext_type is None:
        xtype = ext_type
    else:
        xtype = ''
    return uploadCaseResultFile(gid, sid, tid, filedata, ftype, xtype)

@appweb.route('/group/<gid>/test/<sid>/update',method='POST')
def doUpdateGroupTestSession(gid, sid):
    """
    URL:/group/<gid>/test/<sid>/update
    TYPE:http/POST

    update a test session in group

    @type gid:string
    @param gid:the id of group
    @type sid:string
    @param sid:the id of test session
    @type data:JSON
    @param data:{'token':(string)token,'endtime':(string)endtime, 'status':(string)status}
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
            uid = getUserId(token)
            if uid is None:
                return {'errors':{'code':'01','msg':'Invalid token.'}}
            return updateTestSession(gid, sid, endtime)
        else:
            return {'errors':{'msg':'Invalid params!','code':'03'}}

@appweb.route('/group/<gid>/test/<sid>/delete',method='GET')
def doDeleteGroupTestSession(gid, sid):
    """
    URL:/group/<gid>/test/<sid>/delete
    TYPE:http/GET

    delete a test session from group.

    @type gid:string
    @param gid:the id of group
    @type sid:string
    @param sid:the id of test session
    @type token:string
    @param token:the access token
    @rtype: JSON
    @return:ok-{'results':1}
            error-{'errors':{'code':value,'msg':(string)info}}
    """
    jsond = request.params
    if not jsond is None:
        token = jsond['token']
        uid = getUserId(token)
        if uid is None:
            return {'errors':{'code':'01','msg':'Invalid token.'}}
        return deleteTestSession(gid, sid)
    else:
        return {'errors':{'msg':'Invalid params!','code':'03'}}

@appweb.route('/group/<gid>/test/<sid>/results',method='GET')
def doGetSessionInfo(gid,sid):
    """
    URL:/group/<gid>/test/<sid>/results
    TYPE:http/GET

    Get results of a test session by sid

    @type gid:string
    @param gid:the id of group
    @type sid:string
    @param sid:the id of test session
    @type token:JSON
    @param token:the access token
    @rtype: JSON
    @return:ok-{'results':{'count':(int)count, 'paging':{'pageSize':(int)pageSize,'totalPage':(int)totalPage,'curPage':(int)curPage },'cases':[{'casename':(string)casename, 'starttime':(string)}, 'result':(pass,fail,error), 'log':(string)logfileKey, snaps':[]...]}}
            error-{'errors':{'code':value,'msg':(string)info}}
    """
    jsond = request.params
    if not jsond is None:
        token = jsond['token']
        uid = getUserId(token)
        if uid is None:
            return {'errors':{'code':'01','msg':'Invalid token.'}}
        return getTestSessionInfo(gid,sid)
    else:
        return {"errors":{"msg":"Invalid params!", "code":"03"}}

@appweb.route('/group/<gid>/test/<sid>/case/<tid>/log',method='GET')
def doGetCaseResultLog(gid, sid, tid):
    """
    URL:/group/<gid>/test/<sid>/case/<tid>/log
    TYPE:http/GET

    Get test case log file

    @type gid:string
    @param gid:the id of group
    @type sid:string
    @param sid:the id of test session
    @type  tid: string
    @param tid: the id of case result
    @type data:JSON
    @param data:{'token':(string)value}
    @rtype: JSON
    @return:ok
            error-{'errors':{'code':value,'msg':(string)info}}
    """
    jsond = request.params
    if not jsond is None:
        #token = jsond['token']
        filename = 'log-%s-%s.zip' % (sid,tid)
        response.set_header('Content-Type','application/x-download')
        response.set_header('Content-Disposition','attachment; filename='+filename,True)
        return getTestCaseLog(gid, sid, tid)
    else:
        return {"errors":{"msg":"Invalid params!", "code":"03"}}

@appweb.route('/group/<gid>/test/<sid>/case/<tid>/snaps',method='GET')
def doGetCaseResultSnapshots(gid, sid, tid):
    """
    URL:/group/<gid>/test/<sid>/case/<tid>/snaps
    TYPE:http/GET

    Get detail of a test case result by sid&tid

    @type gid:string
    @param gid:the id of group
    @type sid:string
    @param sid:the id of test session
    @type  tid: string
    @param tid: the id of case result
    @type data:JSON
    @param data:{'token':(string)value}
    @rtype: JSON
    @return:ok-{'results':{snaps:[{'title':(string)title, 'data':(string)base64Data}, {'title':(string)title, 'data':(string)base64Data}]}}
            error-{'errors':{'code':value,'msg':(string)info}}
    """
    jsond = request.params
    if not jsond is None:
        return getTestCaseSnaps(gid,sid,tid)
    else:
        return {"errors":{"msg":"Invalid params!", "code":"03"}}

@appweb.route('/group/<gid>/testsummary',method='GET')
def doGetGroupTestSessions(gid):
    """
    URL:/group/<gid>/testsummary
    TYPE:http/GET

    get sessions summary of a group

    @type gid:string
    @param gid:the id of group
    @type token:string
    @param token:the access token
    @rtype: JSON
    @return:ok-{'results':{'count':(int)count, 'sessions':[ {planname':(string)value,'starttime':(string)value, 'result':{'total':(int)value, 'pass':(int)value, 'fail':(int)value, 'error':(int)value}, 'runtime':(string)value},... ] }}
            error-{'errors':{'code':value,'msg':(string)info}}
    """
    jsond = request.params
    if not jsond is None:
        token = jsond['token']
        uid = getUserId(token)
        if uid is None:
            return {'errors':{'code':'01','msg':'Invalid token.'}}
        return getTestSessionList(gid)
    else:
        return {"errors":{"msg":"Invalid params!", "code":"03"}}

if __name__ == '__main__':
    print 'WebServer Serving on 8080...'
    WSGIServer(("", 8080), appweb).serve_forever()