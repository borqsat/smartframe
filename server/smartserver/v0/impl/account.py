from dbstore import store

TOKEN_EXPIRES = {'01': 999999, '02': 999999, '03': 999, '04': 999}


def userRegister(appid, user, pswd, info):
    rdata = store.createUser(appid, user, pswd, info)
    if 'uid' in rdata:
        return {'results': rdata}
    else:
        return {'errors': rdata}


def userLogin(appid, user, pswd):
    uid = store.userExists(user, pswd)
    if not uid is None:
        rdata = store.createToken(appid, uid, {}, TOKEN_EXPIRES[appid])
        if 'token' in rdata:
            return {'results': rdata}
        else:
            return {'errors': rdata}
    else:
        return {'errors': {'code': '02', 'msg': 'Incorrect UserName/Password or unverified email!'}}


def getUserId(token):
    ret = store.validToken(token)
    if 'uid' in ret:
        return ret['uid']
    else:
        return None


def inviteUser(appid, email, gid, uid):
    info = {'email': email, 'gid': gid}
    rdata = store.createToken(appid, uid, info, TOKEN_EXPIRES[appid])
    if 'token' in rdata:
        return {'results': rdata}
    else:
        return {'errors': rdata}


def activeUser(uid):
    rdata = store.activeUser(uid)
    if 'uid' in rdata:
        return {'results': rdata}
    else:
        return {'errors': {'code': '04', 'msg': 'no user found!'}}


def userChangePassword(uid, oldpswd, newpswd):
    rdata = store.userChangePassword(uid, oldpswd, newpswd)
    if 'uid' in rdata:
        return {'results': rdata}
    else:
        return {'errors': rdata}


def userUpdateInfo(uid, info):
    rdata = store.userUpdateInfo(uid, info)
    if 'uid' in rdata:
        return {'results': rdata}
    else:
        return {'errors': rdata}


def getUserInfo(uid):
    rdata = store.userInfo(uid)
    if 'uid' in rdata:
        return {'results': rdata}
    else:
        return {'errors': rdata}


def userLogout(token):
    rdata = store.deleteToken(token)
    return {'results': 1}


def getUserList():
    rdata = store.getUserList()
    if not rdata is None:
        return {'results': rdata}
    else:
        return {'errors': {'code': '04', 'msg': 'no user found!'}}
