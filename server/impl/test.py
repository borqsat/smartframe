from dbstore import store

def createTestSession(token,sid,planname,starttime, deviceid, deviceinfo):
    ret = store.validToken(token)
    if ret.has_key('uid'):
        uid = ret['uid']
        store.createTestSession(sid, uid, planname, starttime, deviceid, deviceinfo)
        return {'results':1}
    else:
        return {'errors':{'code':'01','msg':'Invalid token.'}}

def updateTestSession(token,sid,endtime):
    ret = store.validToken(token)
    if ret.has_key('uid'):
        uid = ret['uid']
        store.updateTestSession(sid, endtime)
        return {'results':1}
    else:
        return {'errors':{'code':'01','msg':'Invalid token.'}}

def deleteTestSession(token,sid):
    ret = store.validToken(token)
    if ret.has_key('uid'):
        uid = ret['uid']
        store.deleteTestSession(sid)
        return {'results':1}
    else:
        return {'errors':{'code':'01','msg':'Invalid token.'}}

def getTestSessionList(token):
    ret = store.validToken(token)
    if ret.has_key('uid'):
        uid = ret['uid']
        rdata = store.readTestSessionList(uid)
        if not rdata is None :
            return {'results':rdata}
        else:
            return {'errors':{'code':404,'msg':'None reuslt.'}}
    else:
        return {'errors':{'code':'01','msg':'Invalid token.'}}

def getTestSessionInfoEx(sid):
    rdata = store.readTestSessionInfo(sid, '00001')
    if not rdata is None :
        return {'results':rdata}
    else:
        return {'errors':{'code':404,'msg':'None reuslt.'}}

def getTestSessionInfo(token, sid):
    ret = store.validToken(token)
    if ret.has_key('uid'):
        uid = ret['uid']
        rdata = store.readTestSessionInfo(sid, uid)
        if not rdata is None :
            return {'results':rdata}
        else:
            return {'errors':{'code':404,'msg':'None reuslt.'}}
    else:
        return {'errors':{'code':'01','msg':'Invalid token.'}}

def createCaseResult(token,sid,tid,casename,starttime):
    store.createTestCaseResult(sid, tid, casename, starttime)
    return {'results':1}

def getTestCaseInfo(token, sid, tid):
    rdata = store.readTestCaseInfo(sid, tid)
    if not rdata is None :
        return {'results':rdata}
    else:
        return {'errors':{'code':404,'msg':'None reuslt.'}}

def updateCaseResult(token,sid, tid,status,traceinfo, endtime):
    store.updateTestCaseResult(sid, tid, status,traceinfo,endtime)
    return {'results':1}

def uploadCaseResultFile(token, sid, tid, rawdata, ftype='png', ctype=''):
    if ftype == 'png':
        store.writeTestSnapshot(sid, tid, rawdata, ctype)
        return {'results':1}
    elif ftype == 'zip':
        store.writeTestLog(sid, tid, rawdata)
        return {'results':1}
    else:
        return {'errors':{'code':500,'msg':'Invalid ftype value.'}}

def getTestCaseLog(token, sid, tid):
    rdata = store.getCaseLog(sid, tid)
    if not rdata is None :
        return rdata
    else:
        return {'errors':{'code':404,'msg':'None reuslt.'}}

def getTestCaseSnaps(token, sid, tid):
    rdata = store.readTestHistorySnaps(sid, tid)
    if not rdata is None:
        return {'results':rdata}
    else:
        return {'errors':{'code':404,'msg':'None reuslt.'}}

def getTestLiveSnaps(sid):
    imgBuffer = store.readTestLiveSnaps(sid)
    if not imgBuffer is None:
        return imgBuffer
    else:
        return []

def getTestSessionResults(token, sid):
    results = store.readTestLiveResults(sid)
    if not results is None:
        return results
    else:
        return []
