from gevent import monkey; monkey.patch_all()
from bottle import request, response, Bottle
from gevent.pywsgi import WSGIServer
from impl.test import *
from impl.account import *
from impl.group import *
import smtplib

appweb = Bottle()

def sendVerifyMail(receiver, user, token):
    sender   = 'borqsat@borqs.com'  
    subject  = 'Please active your account from SmartAT'
    mailuser = 'borqsat@borqs.com'
    mailpass = '!QAZ2wsx3edc'
      
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, receiver, subject))
    msg = msg+'Hi:\r\n'
    msg = msg+'\r\nThis mail send from smartServer automatically, do not reply this mail directly.\r\n'
    msg = msg+'\r\nYour account \"%s\" has been initialized.\r\n' % (user)
    msg = msg+'\r\nPlease verify your current email via the url as below.\r\n'    
    msg = msg+'\r\nsmart Server: http://ats.borqs.com/smartserver/verify.html?token=%s\r\n' % (token)
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

def err(code='500', msg='Unknown error!'):
    """
    generate error message.
    """
    return {'errors': {'code': code, 'msg': msg}}

# decorator to check if the request has a content-type not in *types.
# if no, then return error message.
# **It must be put after other bottle decorators, like route.**
def content_type(*types):
    def content_type_wrapper(fn):
        def wrapper(*args, **kwargs):
            for t in types:
                if t.lower() in request.content_type:
                    return fn(*args, **kwargs)
            return err(code='500', msg='Invalid content-type header!')
        return wrapper
    return content_type_wrapper

# decorator to check if the request contrains a valid token. The token param may be in query, form or json
# If yes, put the uid in the **kwargs
# **It must be put after other bottle decorators, like route.**
def logined(fn):
    def wrapper(*args, **kwargs):
        uid = None
        if request.params and 'token' in request.params:
            # get token from params and then get uid
            uid = getUserId(request.params['token'])
        elif uid is None and request.json and 'token' in request.json:
            # get token from request.json and then get uid
            uid = getUserId(request.json['token'])
        else:
            # No token param.
            return err('03', 'The API needs a valid "token" parameter. No token provided in the request!')

        if uid is None:
            # if the uid is None, then we return an error message.
            return err('01', 'Invalid token!')
        else:
            # else we add uid to kwargs and then invoke fn
            kwargs['uid'] = uid
            return fn(*args, **kwargs)
    return wrapper

@appweb.route('/account/register',method='POST')
@content_type('application/json')
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
    appid = request.json['appid']
    username = request.json['username']
    password = request.json['password']
    info = request.json['info']
    ret = userRegister(appid, username, password, info)
    if ret.has_key('results'):
        sendVerifyMail(info['email'], username, ret['results']['token'])
    return ret

@appweb.route('/account/changepasswd',method='POST')
@content_type('application/json')
@logined
def doChangePassword(uid):
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
    return userChangePassword(uid, request.json['oldpassword'], request.json['newpassword'])

@appweb.route('/account/update',method='POST')
@content_type('application/json')
@logined
def doUpdateUserInfo(uid):
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
    return userUpdateInfo(uid, request.json['info'])

@appweb.route('/account/invite',method='POST')
@content_type('application/json')
@logined
def doInviteUser(uid):
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
    appid = request.json['appid']
    email = request.json['email']
    username = request.json['username']
    groupname = request.json['groupname']
    gid = request.json['gid']
    rdata = inviteUser(appid, email, gid, uid)
    if rdata.has_key('results'):
        sendInviteMail(email, username, groupname, rdata['results']['token'])
    return rdata

@appweb.route('/account/active',method='POST')
@content_type('application/json')
@logined
def doActiveUser(uid):
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
    rdata = activeUser(uid)
    userLogout(request.json['token'])
    return rdata

@appweb.route('/account/info',method='GET')
@logined
def doGetUserInfo(uid):
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
    return getUserInfo(uid)

@appweb.route('/account/login',method='POST')
@content_type('application/json')
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
    return userLogin(request.json['appid'], request.json['username'], request.json['password'])

@appweb.route('/account/logout',method='GET')
@logined
def doLogout(uid):
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
    return userLogout(request.params['token'])

@appweb.route('/account/list',method='GET')
@logined
def accountlist(uid):
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
    return getUserList()

@appweb.route('/group/create',method='POST')
@content_type('application/json')
@logined
def doCreateGroup(uid):
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
    return createGroup(uid, request.json['groupname'], request.json['info'])

@appweb.route('/group/<gid>/addmember',method='POST')
@content_type('application/json')
@logined
def doAddmemberToGroup(gid, uid):
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
    return addGroupMembers(uid, gid, request.json['members'])

@appweb.route('/group/<gid>/setmember',method='POST')
@content_type('application/json')
@logined
def doSetmemberInGroup(gid, uid):
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
    return setGroupMembers(uid, gid, request.json['members'])

@appweb.route('/group/<gid>/delmember',method='POST')
@content_type('application/json')
@logined
def doRemovememberFromGroup(gid, uid):
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
    #TODO we should check if the uid has the permission to perform the operation
    #including all operations below related with group...
    return delGroupMembers(uid, gid, request.json['members'])

@appweb.route('/group/<gid>/info',method='GET')
@logined
def doGetGroupInfo(gid, uid):
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
    return getGroupInfo(uid, gid)

@appweb.route('/group/<gid>/test/<sid>/create',method='POST')
@content_type('application/json')
@logined
def doCreateGroupTestSession(gid, sid, uid):
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
    return createTestSession(gid, uid, sid, request.json['planname'], request.json['starttime'],
        request.json['deviceid'], request.json['deviceinfo'])

@appweb.route('/group/<gid>/test/<sid>/case/<tid>/create',method='POST')
@content_type('application/json')
@logined
def doCreateCaseResult(gid, sid, tid, uid):
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
    return createCaseResult(gid, sid, tid, request.json['casename'], request.json['starttime'])

@appweb.route('/group/<gid>/test/<sid>/case/<tid>/update',method='POST')
@content_type('application/json')
@logined
def doUpdateCaseResult(gid, sid, tid, uid):
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
    return updateCaseResult(gid, sid, tid, request.json['result'], request.json['traceinfo'], request.json['time'])

@appweb.route('/group/<gid>/test/<sid>/case/<tid>/fileupload', method='PUT')
@content_type('application/json', 'application/zip', 'application/octet-stream')
@logined
def doUploadCaseFile(gid, sid, tid, uid):
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
    if 'image/png' in request.content_type:
        ftype = 'png'
    else:
        ftype = 'zip'

    xtype = request.headers.get('Ext-Type') or ''

    return uploadCaseResultFile(gid, sid, tid, request.body, ftype, xtype)

@appweb.route('/group/<gid>/test/<sid>/update',method='POST')
@content_type('application/json')
@logined
def doUpdateGroupTestSession(gid, sid, uid):
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
    return updateTestSession(gid, sid, request.json['endtime'])

@appweb.route('/group/<gid>/test/<sid>/delete',method='GET')
@logined
def doDeleteGroupTestSession(gid, sid, uid):
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
    #TODO we should check if the uid has the permission to perform the operation
    return deleteTestSession(gid, sid)

@appweb.route('/group/<gid>/test/<sid>/results',method='GET')
@logined
def doGetSessionInfo(gid, sid, uid):
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
    return getTestSessionInfo(gid, sid)

@appweb.route('/group/<gid>/test/<sid>/case/<tid>/log',method='GET')
@logined
def doGetCaseResultLog(gid, sid, tid, uid):
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
    data = getTestCaseLog(gid, sid, tid)
    if type(data) is type({}):
        # if the type of data is a dict, then we got error...
        return data
    else:
        filename = 'log-%s-%s.zip' % (sid, tid)
        response.set_header('Content-Type', 'application/x-download')
        response.set_header('Content-Disposition', 'attachment; filename=' + filename, True)
        return data

@appweb.route('/group/<gid>/test/<sid>/case/<tid>/snaps',method='GET')
@logined
def doGetCaseResultSnapshots(gid, sid, tid, uid):
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
    return getTestCaseSnaps(gid, sid, tid)

@appweb.route('/group/<gid>/testsummary',method='GET')
@logined
def doGetGroupTestSessions(gid, uid):
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
    return getTestSessionList(gid)

if __name__ == '__main__':
    print 'WebServer Serving on 8080...'
    WSGIServer(("", 8080), appweb).serve_forever()
