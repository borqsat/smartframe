from dbstore import store

def userRegister(appid,user,pswd,info):
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
             error-{'errors':{'code':'04','msg':(string)info}} 
    """
    rdata = store.createUser(appid,user,pswd,info)
    if rdata.has_key('uid'):
        return {'results':1}
    else:
        return {'errors':rdata}

def userAuth(appid,user,pswd):
    """
    URL:/user/auth
    TYPE:http/GET

    Get access token by username and password

    @type appid:string
    @param appid:the id of app/domain
    @type user:string
    @param user:the userName of account
    @type pswd:string
    @param pswd:the password of account
    @rtype: JSON
    @return: ok-{'results':{'token':(string)token, 'uid':(string)uid} }
             error-{'errors':{'code':0,'msg':(string)msg}} 
    """
    rdata = store.createToken(appid,user,pswd)
    if rdata.has_key('token'):
        return {'results':rdata}
    else:
        return {'errors':rdata}

def userLogout(token):
    """
    URL:/user/logout
    TYPE:http/GET

    Logout and drop the token

    @type token:string
    @param token:the access token of account
    @rtype: JSON
    @return: ok-{'results':{'token':(string)token, 'uid':(string)uid} }
             error-{'errors':{'code':0,'msg':(string)msg}} 
    """
    rdata = store.deleteToken(token)
    return {'results':1}
