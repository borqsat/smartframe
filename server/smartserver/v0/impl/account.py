#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbstore import store

TOKEN_EXPIRES = {'01': 30*24*3600,
                 '02': 7*24*3600,
                 '03': 24*3600,
                 '04': 24*3600
                 }


def userRegister(appid, user, pswd, info):
    rdata = store.createUser(appid, user, pswd, info)
    if 'uid' in rdata:
        ret = store.createToken(appid, rdata['uid'], {}, TOKEN_EXPIRES[appid])
        rdata['token'] = ret['token']
        return {'results': rdata}
    else:
        return {'errors': rdata}

def forgotPasswd(email):
    ret1 = store.findUserByEmail(email)
    #if not ret1['uid'] is None:
    if not ret1 is None:
        if 'uid' in ret1:
            rdata = {}
            ret = store.createToken('03', ret1['uid'], {}, TOKEN_EXPIRES['03'])
            rdata['token'] = ret['token']
            rdata['uid'] = ret1['uid']
            rdata['password'] = ret1['password']
            return {'results': rdata}
        else:
            return {'errors': {'code': '04', 'msg': 'Invalid or unverified email!'}}
    else:
        return {'errors': {'code': '04', 'msg': 'Invalid or unverified email!'}}

def userLogin(appid, user, pswd):
    uid = store.userExists(user, pswd)
    if not uid is None:
        rdata = store.createToken(appid, uid, {}, TOKEN_EXPIRES[appid])
        if 'token' in rdata:
            return {'results': rdata}
        else:
            return {'errors': rdata}
    else:
        return {'errors': {'code': '02',
                'msg': 'Incorrect UserName/Password or unverified email!'}}


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

def userUpdateAvatar(uid, info):
    rdata = store.writeUserAvatar(uid, info)
    if rdata['ok'] is not None:
        return {'results': rdata}
    else:
        return {'errors': rdata}

def userUpdateInfo(appid, uid, info):
    rdata = store.userUpdateInfo(uid, info)
    if 'uid' in rdata:
        if 'email' in rdata:
            ret = store.createToken(appid, uid, {}, TOKEN_EXPIRES[appid])
            rdata['token'] = ret['token']
        return {'results': rdata}
    else:
        return {'errors': rdata}


def getUserInfo(uid):
    user = store.getUserInfo(uid)

    if user is None:
        return {'errors': {'code': '04', 'msg': 'Invalid User ID!'}}
    else:
        return {'results': user}


def userLogout(token):
    rdata = store.deleteToken(token)
    return {'results': 1}


def getUserList():
    rdata = store.getUserList()
    if not rdata is None:
        return {'results': rdata}
    else:
        return {'errors': {'code': '04', 'msg': 'no user found!'}}
