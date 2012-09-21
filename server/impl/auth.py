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
             error-{'errors':{'code':0,'msg':(string)info}} 
    """
    store.createUser(appid,user,pswd,info)
    return {'results':1}

def userAuth(appid,user,pswd):
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
    rdata = store.createToken(appid,user,pswd)
    if not rdata['token'] is None:
        return {'results':{'token':rdata['token']}}
    else:
        return {'errors':{'code':1, 'msg':'Auth failed!'}}