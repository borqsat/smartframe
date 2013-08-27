#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbstore import store
from random import choice
import string
import hashlib
import uuid
import time

TOKEN_EXPIRES = {'01': 30*24*3600,
                 '02': 7*24*3600,
                 '03': 24*3600,
                 '04': 24*3600
                 }



def doAccountRegister(data):
    pass

def doAccountLogin(data):
    pass

    
def doAccountForgotPassword(data):
    email = data['email']
    if '@' in email:
        collection = 'users'
        findResult = store.doFindOne(collection, spec = {'info.email': email, 'active': True}, fields = {'_id': 0, 'info.email': 1, 'uid': 1})
        
        if not findResult is None:
            uid = str(findResult['uid'])
            newpassword = ''.join([choice(string.ascii_letters+string.digits) for i in range(8)])
            m = hashlib.md5()
            m.update(newpassword)
            updateResult = store.doUpdate(collection, spec={'uid': uid}, fields={'$set': {'password': m.hexdigest()}})
            if updateResult['ok'] != 1.0 and not updateResult['err'] is None:
                return {'errors': {'code': '04', 'msg': 'Reset passwod unsucessfully!!!'}}
            
            rdata = {}
            ret = createToken(appid='03', uid=uid, info={}, expires=TOKEN_EXPIRES['03'])
            rdata['token'] = ret['token']
            rdata['uid'] = uid
            rdata['password'] = newpassword
            print newpassword
            return {'results':rdata}
        else:
            return {'errors': {'code': '04', 'msg': 'Invalid or unverified email!'}}
    else:
        return {'errors': {'code': '04', 'msg': 'Invalid or unverified email!'}}
            
def createToken(appid, uid, info, expires):
    collection = 'tokens'
    m = hashlib.md5()
    m.update(str(uuid.uuid1()))
    token = m.hexdigest()
    result = store.doInsert(collection=collection, spec={'appid': appid, 'uid': uid,'info': info, 'token': token, 'expires': (time.time() + expires)})
    if not result is None:
        return {'token':token, 'uid':uid}
    else:
        return {'errors': {'code': '04', 'msg': 'Insert token unsucessfully!!!'}}


