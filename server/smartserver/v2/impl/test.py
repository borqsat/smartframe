#!/usr/bin/env python
# -*- coding: utf-8 -*-
from account import *

def accountWithOutUid(data):
    
	if data['subc'] == 'register':
		return accountRegister(data['data'])
	elif data['subc'] == 'login':
		return accountLogin(data['data'])
	elif data['subc'] == 'forgotpasswd':
		return accountForgotPasswd(data['data'])

def accountWithUid(uid, data):
	if data['subc'] == 'changepasswd':
		return accountChangepasswd(uid, data['data'])
	elif data['subc'] == 'update':
		return accountUpdate(uid, data['data'])
	elif data['subc'] == 'invite':
		return accountInvite(uid, data['data'])
	elif data['subc'] == 'logout':
		return accountLogout(uid, data['data'])

def getAccountInfo(uid):
	if data['subc'] == 'info':
		return accountGetInfo(uid)
	elif data['subc'] == 'list':
		return accountGetList(uid)


def doGroupAction(data):
	if data['subc'] == 'create':
		return doGroupCreate(data['data'])
	elif data['subc'] == 'delete':
		return doGroupDelete(data['data'])

def memberToGroupAction(gid,data):
	if data['subc'] == 'setmember':
	    return setGroupMembers(gid,data['data'])
	elif data['subc'] == 'addmember':
		return addGroupMembers(gid,data['data'])
	elif data['subc'] == 'delmember':
		return delGroupMembers(gid,data['data'])

def groupInfo(gid,data):
	if data['subc'] =='info':
		return getGroupInfo(gid, data['data'])
	elif data['subc'] == 'testsummary':
		return getTestSessionSummary(gid, data['data'])

def testSessionAction(gid,sid,data):
	if data['subc'] =='create':
		return createTestSession(gid,sid,data['data'])
	elif data['subc'] =='update':
		return updateTestSession(gid,sid,data['data'])
	elif data['subc'] == 'delete':
		return deleteTestSession(gid,sdi,data['data'])

def getSessionAction(gid,sid,data):
	if data['subc'] =='results':
		return getSessionAllresults(gid,sid,data['data'])
	elif data['subc'] == 'getcase':
		return getSessionLive(gid,sid,data['data'])
	elif data['subc'] =='summary':
		return getSessionSummary(gid,sid,data['data'])

def caseResultAction(gid,sid,tid,data):
	if data['subc'] == 'create':
		return createTestCaseResult(gid,sid,tid,data['data'])
	elif data['subc'] == 'update':
		return updateTestCaseResult(gid,sid,tid,data['data'])

def getTestLiveSnaps(gid, sid, timestamp):
    return None
