#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbstore import store
from ..sendmail import sendForgotPasswdMail
from business import *


    
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
