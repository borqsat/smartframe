#!/usr/bin/env python
# -*- coding: utf-8 -*-

from business import *

def doAccountBasicActionBeforeLogin(data):
    if data['action'] == 'register':
        return doAccountRegister(data['data'])
    if data['action'] == 'login':
       return doAccountLogin(data['data'])
    if data['action'] == 'forgotpasswd':
        return doAccountForgotPasswd(data['data'])

def doAccountBasicActionAfterLogin(uid, data):
    if data['action'] == 'changepasswd':
        return doAccountChangepasswd(uid, data['data'])
    elif data['action'] == 'update':
        return doAccountUpdate(uid, data['data'])
    elif data['action'] == 'invite':
        return doAccountInvite(uid, data['data'])
    elif data['action'] == 'logout':
        return doAccountLogout(uid, data['data'])

def doAccountGetAction(uid, data):
    if data['action'] == 'info':
        return doAccountGetInfo(uid, data['data'])
    elif data['action'] == 'list':
        return doAccountGetList(uid, data['data'])

def doGroupBasicAction(data):
    if data['action'] == 'create':
        return doGroupCreate(data['data'])
    elif data['action'] == 'delete':
        return doGroupDelete(data['data'])

def doGroupMemeberAction(gid,data):
    if data['action'] == 'setmember':
        return setGroupMembers(gid,data['data'])
    elif data['action'] == 'addmember':
        return addGroupMembers(gid,data['data'])
    elif data['action'] == 'delmember':
        return delGroupMembers(gid,data['data'])

def doGroupGetAction(gid,data):
    if data['action'] =='info':
        return getGroupInfo(gid, data['data'])
    elif data['action'] == 'testsummary':
        return getTestSessionSummary(gid, data['data'])

def doTestSessionBasicAction(gid,sid,data):
    if data['action'] =='create':
        return createTestSession(gid,sid,data['data'])
    elif data['action'] =='update':
        return updateTestSession(gid,sid,data['data'])
    elif data['action'] == 'delete':
        return deleteTestSession(gid,sdi,data['data'])

def doTestSessionGetAction(gid,sid,data):
    if data['action'] =='results':
        return getSessionAllresults(gid,sid,data['data'])
    elif data['action'] == 'getcase':
        return getSessionLive(gid,sid,data['data'])
    elif data['action'] =='summary':
        return getSessionSummary(gid,sid,data['data'])

def doTestCaseBasicAction(gid,sid,tid,data):
    if data['action'] == 'create':
        return createTestCaseResult(gid,sid,tid,data['data'])
    elif data['action'] == 'update':
        return updateTestCaseResult(gid,sid,tid,data['data'])
