from dbstore import store

def createTestSession(gid, uid, sid, planname,starttime, deviceid, deviceinfo):
    store.createTestSession(gid, sid, uid, planname, starttime, deviceid, deviceinfo)
    return {'results':1}

def updateTestSession(gid, sid, endtime):
    store.updateTestSession(gid, sid, endtime)
    return {'results':1}

def deleteTestSession(gid, sid):
    store.deleteTestSession(gid, sid)
    return {'results':1}

def getTestSessionList(gid):
    rdata = store.readTestSessionList(gid)
    if not rdata is None :
        return {'results':rdata}
    else:
        return {'errors':{'code':404,'msg':'None reuslt.'}}

def getTestSessionInfo(gid, sid):
    rdata = store.readTestSessionInfo(gid, sid)
    if not rdata is None :
        return {'results':rdata}
    else:
        return {'errors':{'code':404,'msg':'None reuslt.'}}

def createCaseResult(gid, sid,tid,casename,starttime):
    store.createTestCaseResult(gid, sid, tid, casename, starttime)
    return {'results':1}

def getTestCaseInfo(gid, sid, tid):
    rdata = store.readTestCaseInfo(gid, sid, tid)
    if not rdata is None :
        return {'results':rdata}
    else:
        return {'errors':{'code':404,'msg':'None reuslt.'}}

def updateCaseResult(gid, sid, tid,status,traceinfo, endtime):
    store.updateTestCaseResult(gid, sid, tid, status,traceinfo,endtime)
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

def getTestCaseLog(gid, sid, tid):
    rdata = store.getCaseLog(gid, sid, tid)
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

def getTestLiveSnaps(gid, sid):
    imgBuffer = store.readTestLiveSnaps(gid, sid)
    if not imgBuffer is None:
        return imgBuffer
    else:
        return []
