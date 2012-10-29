#!/usr/bin/env python

from pymongo import Connection
import gridfs
import memcache
import hashlib,uuid,base64
from bson.objectid import ObjectId

class dbStore(object):
    """
    Class dbStore provides the access to MongoDB DataBase
    """
    def __init__(self, server='192.168.7.212', port=27017):
        """
        do the database instance init works
        """
        print 'init db store class!!!'
        self.db = Connection(server, port)['smartServer']
        self.fs = gridfs.GridFS(Connection(server, port)['smartGridFS'], collection='rawfiles')
        self.mc = memcache.Client(['127.0.0.1:11211'],debug=0)
        self.snapqueue = {}

    def getfile(self,fileId): 
        '''
        Get file.
        '''
        data = None
        objId = ObjectId(fileId)
        exists = self.fs.exists(objId)
        if exists:
            data = self.fs.get(objId)
        return data

    def createUser(self,appid,user,password,info):
        """
        write a user account record in database
        """
        m = hashlib.md5()
        m.update(password)
        users = self.db['user']
        uid = str(uuid.uuid1())
        users.insert({'uid':uid,'appid':appid,'username':user,'password':m.hexdigest(),'info':info});

    def validToken(self, token):
        uid = ''
        username = ''
        tokens = self.db['token']
        rdata = tokens.find({'token':token})
        for t in rdata:
            uid = t['uid']
        
        if uid != '':
            users = self.db['user']
            rdata = users.find({'uid':uid})
            for t in rdata:
                username = t['username']
            return {'uid':uid, 'username':username}  
        else:
            return {'code':2, 'msg':'Invalid token!'} 

    def createToken(self,appid,user,password):
        """
        write a user account record in database
        """
        users = self.db['user']
        ret = users.find({'appid':appid,'username':user,'password':password})
        uid = ''
        token = ''
        for d in ret:
            uid = d['uid']
            tokens = self.db['token']
            rdata = tokens.find({'uid':uid})
            for t in rdata:
                token = t['token']
            if token == '':
                token = str(uuid.uuid1())
                tokens.insert({'uid':uid,'token':token,'expires':'2000'})

        if token == '':
            return {'code':1, 'msg':'user or password is incorrect!'}              
        else:
            return {'token':token,'uid':uid}

    def createTestSession(self, sid, uid, planname, starttime, deviceid, devinfo):
        """
        write a test session record in database
        """
        session = self.db['session']
        session.insert({'sid':sid,
                       'uid':uid, 
                       'planname':planname,
                       'result':{'total':0,'pass':0,'fail':0,'error':0},
                       'starttime':starttime,
                       'endtime': 'N/A', 
                       'runtime': 0,
                       'deviceid':deviceid,
                       'deviceinfo':devinfo
                      });

    def updateTestSession(self,sid,endtime):
        """
        write a test session record in database
        """
        session = self.db['session']
        session.update({'sid':sid},{'$set':{'endtime':endtime}});        

    def deleteTestSession(self,sid):
        """
        delete a test session from database
        """
        caseresult = self.db['caseresult']
        caseresult.remove({'sid':sid});       
        session = self.db['session']
        session.remove({'sid':sid});

    def readTestSessionList(self, uid):
        """
        read list of test session records in database
        """
        session = self.db['session']
        rdata = session.find({'uid':uid})
        result = {}
        lists = [{'sid':d['sid'],
                'uid':d['uid'],
                'planname':d['planname'],
                'result':d['result'],
                'starttime':d['starttime'],
                'endtime':d['endtime'],
                'runtime':d['runtime'],
                'deviceid':d['deviceid'],
                'deviceinfo':d['deviceinfo']} for d in rdata]
        result['count'] = len(lists)
        result['sessions'] = lists
        return result

    def readTestSessionInfo(self,sid,uid):
        """
        read list of test session records in database
        """
        session = self.db['session']
        rdata = session.find({'sid':sid, 'uid':uid})
        for d in rdata:
            result = {'sid':d['sid'],
                      'planname':d['planname'],
                      'result':d['result'],
                      'starttime':d['starttime'],
                      'endtime':d['endtime'],
                      'runtime':d['runtime'],
                      'deviceid':d['deviceid'],
                      'deviceinfo':d['deviceinfo']}
        caseresult = self.db['caseresult']
        rdata = caseresult.find({'sid':sid})
        lists = [{'tid':d['tid'],
                'sid':d['sid'],
                'casename':d['casename'],
                'starttime':d['starttime'],
                'endtime':d['endtime'],
                'traceinfo':d['traceinfo'],
                'result':d['result']} for d in rdata]
        result['count'] = len(lists)
        result['cases'] = lists
        return result

    def readTestCaseInfo(self, sid, tid):
        """
        read list of test cases records in database
        """
        caseresult = self.db['caseresult']
        ret = caseresult.find({'sid':sid,'tid':tid})
        result = None
        for d in ret:
            if not 'result' in d :
                d['result'] = ''
            if not 'log' in d :
                d['log'] = ''
            if not 'snapshots' in d:
                d['snapshots'] = []
            if not 'checksnap' in d:
                d['checksnap'] = ''

            result = {'tid':d['tid'],
                    'casename':d['casename'],
                    'starttime':d['starttime'],
                    'endtime':d['endtime'],
                    'result':d['result'],
                    'traceinfo':d['traceinfo'],
                    'log':d['log'],
                    'snapshots':d['snapshots'],
                    'checksnap':d['checksnap']}
        return result

    def getCaseLog(self, sid, tid):
        """
        read list of test session records in database
        """
        caseresult = self.db['caseresult']
        ret = caseresult.find({'sid':sid,'tid':tid})
        result = None
        logid = None
        for d in ret:
            logid = d['log'] 
        if not logid is None:
            result = self.getfile(logid)
        return result

    def createTestCaseResult(self,sid,tid,casename,starttime):
        """
        write a test case resut record in database
        """
        self.snapquene[sid+'-'+tid] = []
        self.mc.set(sid+'id',tid)
        self.mc.set(sid+'name',casename)
        self.mc.set(sid+'status','start')
        caseresult = self.db['caseresult']
        caseresult.insert({'sid':sid, 'tid':tid, 'casename':casename, 'log':'N/A', 'traceinfo':'N/A','result':'running', 'starttime':starttime, 'endtime':'N/A','snapshots':[], 'checksnap':''})
        session = self.db['session']
        session.update({'sid':sid},{'$inc':{'result.total':1}})

    def updateTestCaseResult(self, sid, tid, status, traceinfo, endtime):
        """
        update a test case resut record in database
        If case get failed, write snapshot png files in GridFS
        """
        caseresult = self.db['caseresult']
        session = self.db['session']
        status = status.lower()
        self.mc.set(sid+'status','result->'+status)
        if status == 'pass':
            session.update({'sid':sid},{'$inc':{'result.pass':1}})
        elif status == 'fail':
            session.update({'sid':sid},{'$inc':{'result.fail':1}})               
        else:
            session.update({'sid':sid},{'$inc':{'result.error':1}})

        caseresult.update({'sid':sid,'tid':tid},{'$set':{'result':status,'traceinfo':traceinfo,'endtime':endtime}})

    def writeTestLog(self,sid, tid,logfile):
        """
        add log file in GridFS
        update the corresponding test case resut record
        """
        caseresult = self.db['caseresult']
        log = self.fs.put(logfile)
        caseresult.update({'sid':sid,'tid':tid},{'$set':{'log':str(log)}})

    def writeTestSnapshot(self,sid, tid, snapfile, stype):
        """
        add snapshot png in image buffer
        """
        if self.mc:
            self.mc.set(sid+'snap', snapfile)

        if not (sid+'-'+tid) in self.snapquene:
            self.snapquene[sid+'-'+tid] = []
        try:
            idx = self.fs.put(snapfile)
            caseresult = self.db['caseresult']            
            if stype == 'check':
                checksnap = str(idx)
                caseresult.update({'sid':sid,'tid':tid},{'$set':{'checksnap':checksnap}})
            else:
                self.snapquene[sid+'-'+tid].append(str(idx))
                snapshots = self.snapquene[sid+'-'+tid]
                caseresult.update({'sid':sid,'tid':tid},{'$set':{'snapshots':snapshots}})
        except:
            pass

    def readTestLiveSnaps(self,sid):
        result = []
        rdata = self.mc.get(sid+'snap')
        result.append(rdata)
        return result

    def readTestLiveResults(self,sid):
        result = []
        tid = self.mc.get(sid+'id')
        tname = self.mc.get(sid+'name')
        tstatus = self.mc.get(sid+'status')
        if not tid is None:
            result.append('id:%s, casename:%s, status:%s' % (tid,tname,tstatus))   
        return result

    def readTestHistorySnaps(self,sid, tid):
        caseresult = self.db['caseresult']
        ret = caseresult.find({'sid':sid,'tid':tid})
        snapids = []
        snaps = []
        checkid = ''
        checksnap = ''
        for d in ret:
            snapids = d['snapshots']
            if not 'checksnap' in d:
                checkid = ''
            else:
                checkid = d['checksnap']

        for fid in snapids:
            fs = self.getfile(fid)
            if not fs is None:
                snaps.append(base64.encodestring(fs.read()))
        
        if checkid != '':
            fs = self.getfile(checkid)
            if not fs is None:
                checksnap = base64.encodestring(fs.read())         

        return {'snaps':snaps, 'checksnap':checksnap}

store = dbStore(server='192.168.7.212', port=27017)