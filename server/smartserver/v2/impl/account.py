#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import time
import uuid
import string
from random import choice
from dbstore import store
from ..sendmail import *

TOKEN_EXPIRES = {'01': 30*24*3600,
                 '02': 7*24*3600,
                 '03': 24*3600,
                 '04': 24*3600
                 }

def counter(keyname):
    query = {'_id': keyname}
    update = {'$inc': {'next': 1}}
    return int(store.doFind_and_Modify('counter', query, update)['next'])

def createToken(appid, uid, info, expires):
    collection = 'tokens'
    m = hashlib.md5()
    m.update(str(uuid.uuid1()))
    token = m.hexdigest()
    result = store.doInsert(collection=collection, doc={'appid': appid, 'uid': uid,'info': info, 'token': token, 'expires': (time.time() + expires)})
    if not result is None:
        return {'token':token, 'uid':uid}
    else:
        return {'errors': {'code': '04', 'msg': 'Insert token unsucessfully!!!'}}

def accountRegister(data):
    if len(store.doFind('users', {'username': data['username']})) == 0 & len(store.doFind('users', {'info.email': data['info']['email']})) == 0:
        m = hashlib.md5()
        m.update(data['password'])
        pswd = m.hexdigest()
        m.update('%08d' % counter('userid'))
        uid = m.hexdigest()

        userDoc = {'uid': uid, 'appid': data['appid'], 'username':data['username'], 
               'password': pswd, 'active': False, 'info': data['info']}
        store.doInsert('users', userDoc)

        ret = createToken(appid=data['appid'], uid=uid, info={},expires=TOKEN_EXPIRES[data['appid']])

        sendVerifyMail(data['info']['email'], data['username'], ret['token'])
        return {'results': 'ok', 'data': {'token': ret['token'], 'uid': uid}, 'msg': ''}
    else:
        return {'results': 'error', 'data': {'code': '04'}, 'msg': 'An account with same email or username already registered!'}

def accountLogin(data):
    if '@' in data['username']:
        spec = {'info.email': data['username'], 'password': data['password'], 'active': True}
    else:
        spec = {'username': data['username'], 'password': data['password']}

    fields = {'_id': 0, 'uid': 1}
    result = store.doFind('users', spec, fields)
    
    if len(result) != 0:        
        ret = createToken(appid=data['appid'], uid=result[0]['uid'], info={},expires=TOKEN_EXPIRES[data['appid']])
        return {'results': 'ok', 'data': {'token': ret['token'], 'uid': result[0]['uid']}, 'msg': ''}
    else:
        return {'results': 'error', 'data':{'code': '02'}, 'msg': 'Incorrect UserName/Password or unverified email!'}

def accountForgotPasswd(data):
    email = data['email']
    if '@' in email:
        collection = 'users'
        findResult = store.doFindOne(collection, spec = {'info.email': email, 'active': True}, fields = {'_id': 0, 'info.email': 1, 'uid': 1})
        
        if not findResult is None:
            uid = str(findResult['uid'])
            newpassword = ''.join([choice(string.ascii_letters+string.digits) for i in range(8)])
            m = hashlib.md5()
            m.update(newpassword)
            updateResult = store.doUpDate(collection, spec={'uid': uid}, doc={'$set': {'password': m.hexdigest()}})
            if updateResult['ok'] != 1.0 and not updateResult['err'] is None:
                return {'errors': {'code': '04', 'msg': 'Reset passwod unsucessfully!!!'}}
            
            rdata = {}
            ret = createToken(appid='03', uid=uid, info={}, expires=TOKEN_EXPIRES['03'])
            rdata['token'] = ret['token']
            rdata['uid'] = uid
            rdata['password'] = newpassword
            print newpassword
#             sendForgotPasswdMail(email, newpassword, ret['token'])
            return {'results': 'ok','data':rdata,'msg':''}
        else:
            return {'results':'error','data': {'code': '04'}, 'msg': 'Invalid or unverified email!'}
    else:
        return {'results':'error','data': {'code': '04'},'msg': 'Invalid or unverified email!'}

def accountChangepasswd(uid,data):
    m = hashlib.md5()
    m.update(data['oldpassword'])
    print 'uid' + uid
    spec={'uid':uid}
    fields = {'_id': 0, 'password': 1}
    result = store.doFind('users', spec, fields)
    
    print result
    if m.hexdigest() == result[0]['password']:
        m = hashlib.md5()
        m.update(data['newpassword'])
        doc ={'$set':{'password': m.hexdigest()}}
        store.doUpDate('users',spec,doc)
        return {'results': 'ok','data':{'uid': uid},'msg':''}
    else:
        return {'results':'error','data': {'code': '03'},'msg': 'Incorrect original password!'}