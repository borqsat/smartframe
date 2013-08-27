#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()

from bottle import request, response, Bottle, HTTPResponse
from gevent.pywsgi import WSGIServer

from .impl.test import *
from .impl.account import *
from .impl.group import *
from .sendmail import sendVerifyMail, sendInviteMail, sendForgotPasswdMail
from .plugins import LoginPlugin, ContentTypePlugin

from .. import tasks

appweb = Bottle()

contenttype_plugin = ContentTypePlugin()
appweb.install(contenttype_plugin)

login_plugin = LoginPlugin(getuserid=getUserId,
                           request_token_param="token",
                           login=True)  # login is required by default
appweb.install(login_plugin)


@appweb.route('/account', method='POST', content_type='application/json', login=False)
def doForgotpasswd():
    """
    URL:/account
    TYPE:http/POST
    @type data:JSON
    @param data:{'subc': '', 'data':{}}
    @rtype: JSON
    @return: ok-{'results':'ok', 'data':{}, 'msg': ''}
             error-{'results':'error', 'data':{'code':(string)code}, 'msg': '(string)info'}
    ---------------------------------------------------------------------------------------
    |support|subc          |data
    |       |register      |{'username':(string)username, 'password':(string)password, 'appid':(string)appid,'info':{'email':(string), 'telephone':(string)telephone, 'company':(string)company}
    |       |forgotpasswd  |{'email':(string)mailaddress}
    |       |login         |{'appid':(int)appid, 'username':(string)username, 'password':(string)password}
    ---------------------------------------------------------------------------------------
    """
    return doAccountBasicActionBeforeLogin(request.json)


if __name__ == '__main__':
    print 'WebServer Serving on 8080...'
    WSGIServer(("", 8080), appweb).serve_forever()
