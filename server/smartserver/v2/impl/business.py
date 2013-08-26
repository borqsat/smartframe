#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import time
import uuid
from dbstore import store
from ..sendmail import *

TOKEN_EXPIRES = {'01': 30*24*3600,
                 '02': 7*24*3600,
                 '03': 24*3600,
                 '04': 24*3600
                 }

def generateToken():
    m = hashlib.md5()
    m.update(str(uuid.uuid1()))
    token = m.hexdigest()
    return token

def counter(keyname):
    query = {'_id': keyname}
    update = {'$inc': {'next': 1}}
    return int(store.doFind_and_Modify('counter', query, update)['next'])

def doAccountLogin(data):
    if '@' in data['username']:
        spec = {'info.email': data['username'], 'password': data['password'], 'active': True}
    else:
        spec = {'username': data['username'], 'password': data['password']}

    fields = {'_id': 0, 'uid': 1}
    result = store.doFind('users', spec, fields)
    
    if len(result) != 0:
        token = generateToken()
        doc = {'appid': data['appid'], 'uid': result[0]['uid'],
               'info': {}, 'token': token, 'expires': (time.time() + TOKEN_EXPIRES[data['appid']])}
        
        store.doInsert('tokens', doc)
        return {'results': 'ok', 'data': {'token': token, 'uid': result[0]['uid']}, 'msg': ''}
    else:
        return {'results': 'error', 'data':{'code': '02'}, 'msg': 'Incorrect UserName/Password or unverified email!'}
        
def doAccountRegister(data):
    if len(store.doFind('users', {'username': data['username']})) == 0 & len(store.doFind('users', {'info.email': data['info']['email']})) == 0:
        m = hashlib.md5()
        m.update(data['password'])
        pswd = m.hexdigest()
        m.update('%08d' % counter('userid'))
        uid = m.hexdigest()

        userDoc = {'uid': uid, 'appid': data['appid'], 'username':data['username'], 
               'password': pswd, 'active': False, 'info': data['info']}
        store.doInsert('users', userDoc)

        token = generateToken()
        tokenDoc = {'appid': data['appid'], 'uid': uid, 'info': {}, 
                    'token': token, 'expires': (time.time() + TOKEN_EXPIRES[data['appid']])}
        store.doInsert('tokens', tokenDoc)

        sendVerifyMail(data['info']['email'], data['username'], token)
        return {'results': 'ok', 'data': {'token': token, 'uid': uid}, 'msg': ''}
    else:
        return {'results': 'error', 'data': {'code': '04'}, 'msg': 'An account with same email or username already registered!'}
