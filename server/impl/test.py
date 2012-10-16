from dbstore import store

def createTestSession(token,sid,planname,starttime, deviceid, deviceinfo):
    store.createTestSession(sid, planname, starttime, deviceid, deviceinfo)
    return {'results':1}

def updateTestSession(token,sid,endtime):
    store.updateTestSession(sid, endtime)
    return {'results':1}

def deleteTestSession(token,sid):
    store.deleteTestSession(sid)
    return {'results':1}

def getTestSessionList(token):
    rdata = store.readTestSessionList()
    if not rdata is None :
        return {'results':rdata}
    else:
        return {'errors':{'code':404,'msg':'None reuslt.'}}

def getTestSessionInfo(token, sid):
    rdata = store.readTestSessionInfo(sid)
    if not rdata is None :
        return {'results':rdata}
    else:
        return {'errors':{'code':404,'msg':'None reuslt.'}}

def createCaseResult(token,sid,tid,casename,starttime):
    store.createTestCaseResult(sid, tid, casename, starttime)
    return {'results':1}

def getTestCaseInfo(token, sid, tid):
    rdata = store.readTestCaseInfo(sid, tid)
    if not rdata is None :
        return {'results':rdata}
    else:
        return {'errors':{'code':404,'msg':'None reuslt.'}}

def updateCaseResult(token,sid, tid,status):
    store.updateTestCaseResult(sid, tid, status)
    return {'results':1}

def uploadCaseResultFile(token, sid, tid, rawdata, ftype='png'):
    if ftype == 'png':
        store.writeTestSnapshot(sid, tid, rawdata)
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
    imgBuffer = store.readTestHistorySnaps(sid, tid)
    if not imgBuffer is None:
        return imgBuffer
    else:
        return []

def getTestSessionSnaps(token, sid):
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