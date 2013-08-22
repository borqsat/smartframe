#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbstore import store

#{'appid':(int)appid, 'username':(string)username, 'password':(string)password}

def doAccountLogin(data):
    if '@' in data['username']:
        fields = {'info.email': data['username'], 'password': data['password'], 'active': True}
    else:
        fields = {'username': data['username'], 'password': data['password']}
    result = store.usersFind(fields)
    if len(result) == 0:
        return {'results': 'error', 'data':{'code': '02'}, 'msg': 'Incorrect UserName/Password or unverified email!'}
    else:
        return {'results': 'ok', 'data': result[0], 'msg': ''}

