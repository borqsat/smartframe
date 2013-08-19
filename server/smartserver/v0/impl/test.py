#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbstore import store

def createTestSession(gid, uid, sid, value):
    store.createTestSession(gid, sid, uid, value)
    return {'results':1}

def updateTestSession(gid, sid, value):
    store.updateTestSession(gid, sid, value)
    return {'results':1}     

def deleteTestSession(uid, gid, sid):
    from .group import isGroupAdmin
    if not isGroupAdmin(uid, gid):
        return {'errors':{'code':'00','msg':'Admin permission required!'}}

    store.deleteTestSession(gid, sid)
    return {'results':1}

def getTestSessionList(gid):

    rdata = store.readTestSessionList(gid)
    #if not rdata['results'] is None :
    if len(rdata['results'])>0 :
        #return {'results':rdata}
        return rdata
    else:
        return {'errors':{'code':404,'msg':'None result.'}}

def getTestCycleReport(gid,cid):

    rdata = store.readTestReport(gid,cid)
    if not rdata is None :
        return {'results':rdata}
    else:
        return {'errors':{'code':404,'msg':'None result.'}}

def getTestSessionInfo(gid, sid):
    rdata = store.readTestSessionInfo(gid, sid)
    if not rdata is None :
        return {'results':rdata}
    else:
        return {'errors':{'code':404,'msg':'None result.'}}

def isSessionUpdated(gid,sid,tid):
    return {'results':store.isSessionUpdated(gid,sid,tid)}

def getSessionLive(gid,sid,maxCount):
    return {'results':store.getSessionLiveCases(gid,sid,maxCount)}

def getSessionHistory(gid,sid,type,page,pagesize):
    result = store.getSessionAllCases(gid,sid,type,page,pagesize)
    if result is None:
        return {'errors':{'code':404,'msg':'None result.'}}
    else:
        return {'results':result}

def getSessionSummary(gid,sid):
    result = store.getSessionSummary(gid,sid)
    if result is None:
        return {'errors':{'code':404,'msg':'None result.'}}
    else:
        return {'results':result}

def createCaseResult(gid, sid, tid, casename, starttime):
    store.createTestCaseResult(gid, sid, tid, casename, starttime)
    return {'results':1}

def getTestCaseInfo(gid, sid, tid):
    rdata = store.readTestCaseInfo(gid, sid, tid)
    if not rdata is None :
        return {'results':rdata}
    else:
        return {'errors':{'code':404,'msg':'None reuslt.'}}

def updateCaseResult(gid, sid, tid,results):
    store.updateTestCaseResult(gid, sid, tid, results)
    return {'results':1}

def uploadCaseResultFile(gid, sid, tid, rawdata, ftype='png', ctype=''):
    if ftype == 'png':
        store.writeTestSnapshot(gid, sid, tid, rawdata, ctype)
        return {'results':1}
    elif ftype == 'zip':
        store.writeTestLog(gid, sid, tid, rawdata)
        return {'results':1}
    else:
        return {'errors':{'code':500,'msg':'Invalid ftype value.'}}

def getTestCaseLog(fid):
    rdata = store.getCaseLog(fid)
    if not rdata is None :
        return rdata
    else:
        return {'errors':{'code':404,'msg':'None reuslt.'}}

def getTestCaseSnaps(gid, sid, tid):
    rdata = store.readTestHistorySnaps(gid, sid, tid)
    if not rdata is None:
        return {'results':rdata}
    else:
        return {'errors':{'code':404,'msg':'None reuslt.'}}

def getTestCaseSnap(fid):
    rdata = store.readTestCaseSnap(fid)
    if not rdata is None:
        return rdata
    else:
        return {'errors':{'code':404,'msg':'None reuslt.'}}

def getTestLiveSnaps(gid, sid, timestamp):
    imgBuffer = store.readTestLiveSnaps(gid, sid, timestamp)
    return imgBuffer

def checkErrorCount(sid):
    errorCount = store.checkErrorCount(sid)
    return errorCount

def checkMailListAndContext(gid,sid,tid):
    context = store.checkMailListAndContext(gid,sid,tid)
    return context

def getReportData(token):
    result = store.getReportData(token)
    if result:
        return {'results': result}
    else:
        return {'error': {'msg': 'Invalid request or the report has expired!'}}

def getUserMailAddress(token):
    address = store.getUserMailAddress(token)
    if address:
        return address
    else:
        return ''