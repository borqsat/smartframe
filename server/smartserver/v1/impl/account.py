#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbstore import store
from ..sendmail import sendForgotPasswdMail
from business import *

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

    
def doAccountBasicActionBeforeLogin(data):
    
    action = data['action']
    actionDic = {'register' : doAccountRegister(data['data']),
                 'login' : doAccountLogin(data['data']),
                 'forgotpasswd' : doAccountForgotPassword(data['data'])
                 }
     
    result = lambda action: actionDic[action]
    
    ret = result(action)
    if action == 'forgotpasswd' and 'results' in ret:
        sendForgotPasswdMail(data['data']['email'], ret['results']['password'], ret['results']['token'])
        
    return ret
    

def getUserId(token):
    ret = store.validToken(token)
    if 'uid' in ret:
        return ret['uid']
    else:
        return None
