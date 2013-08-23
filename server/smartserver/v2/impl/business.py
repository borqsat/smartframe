#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import time
import uuid
from dbstore import store

TOKEN_EXPIRES = {'01': 30*24*3600,
                 '02': 7*24*3600,
                 '03': 24*3600,
                 '04': 24*3600
                 }

def doAccountLogin(data):
    if '@' in data['username']:
        spec = {'info.email': data['username'], 'password': data['password'], 'active': True}
    else:
        spec = {'username': data['username'], 'password': data['password']}

    fields = {'_id': 0, 'uid': 1}
    result = store.doFind('users', spec, fields)
    
    if len(result) != 0:
        m = hashlib.md5()
        m.update(str(uuid.uuid1()))
        token = m.hexdigest()
        doc = {'appid': data['appid'], 'uid': result[0]['uid'],
               'info': {}, 'token': token, 'expires': (time.time() + TOKEN_EXPIRES[data['appid']])}
        
        store.doInsert('tokens', doc)
        return {'results': 'ok', 'data': {'token': token, 'uid': result[0]['uid']}, 'msg': ''}
    else:
        return {'results': 'error', 'data':{'code': '02'}, 'msg': 'Incorrect UserName/Password or unverified email!'}
        
