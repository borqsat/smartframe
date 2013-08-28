#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smartserver.v2.impl.account as t


if __name__ == '__main__':
    print t.accountLogin({'subc': 'login', 'data': {'appid': '02', 'username': 'b260', 'password': 'e10adc3949ba59abbe56e057f20f883e'}})
    print t.accountRegister({'subc': 'register', 'data':{'username': 'GUO', 'password': '123456', 'appid': '01', 'info': {'email': 'spritegzq@gmail.com'}}})
    print t.accountForgotPasswd({'subc': 'forgotpasswd', 'data':{'email':'rui.huang@borqs.com'}})
    print t.accountChangepasswd({'subc': 'changepasswd', 'data':{'token':'98166813da6fb15c8e201e34e9dfc65c','oldpassword':'123','newpassword':'1234'}}) 