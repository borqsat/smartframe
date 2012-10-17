#!/usr/bin/env python

from pymongo import Connection
import gridfs
import memcache
import mimetypes
import json
import datetime,time
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
        self.imgBuffer = {}

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

    def createToken(self,appid,user,password):
        """
        write a user account record in database
        """
        users = self.db['user']
        ret = users.find({'appid':appid,'username':user,'password':password})
        if len(ret) > 0:
            for d in ret:
                uid = d['uid'] 
            tokens = self.db['token']
            rdata = tokens.find({'uid':uid})
            if not rdata is None:
                for d in rdata:
                    token = d['token']
            else:
                token = str(uuid.uuid1())
                tokens.insert({'uid':uid,'token':token})
            return {'token':token,'uid':uid}
        else:
            return {'code':1, 'msg':'user or password is incorrect!'}

    def createTestSession(self,sid, planname, starttime, deviceid, devinfo):
        """
        write a test session record in database
        """
        session = self.db['session']
        session.insert({'sid':sid,
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

    def readTestSessionList(self):
        """
        read list of test session records in database
        """
        session = self.db['session']
        rdata = session.find()
        lists = [{'sid':d['sid'],
                'planname':d['planname'],
                'result':d['result'],
                'starttime':d['starttime'],
                'endtime':d['endtime'],
                'runtime':d['runtime'],
                'deviceid':d['deviceid'],
                'deviceinfo':d['deviceinfo']} for d in rdata]
        result = {}
        result['count'] = len(lists)
        result['sessions'] = lists
        return result

    def readTestSessionInfo(self,sid):
        """
        read list of test session records in database
        """
        session = self.db['session']
        rdata = session.find({'sid':sid})
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

            result = {'tid':d['tid'],
                    'casename':d['casename'],
                    'starttime':d['starttime'],
                    'endtime':d['endtime'],
                    'result':d['result'],
                    'traceinfo':d['traceinfo'],
                    'log':d['log'],
                    'snapshots':d['snapshots']}
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
        self.imgBuffer[sid+'-'+tid] = []
        self.mc.set(sid+'id',tid)
        self.mc.set(sid+'name',casename)
        self.mc.set(sid+'status','start')
        caseresult = self.db['caseresult']
        caseresult.insert({'sid':sid, 'tid':tid, 'casename':casename, 'log':'N/A', 'traceinfo':'N/A','result':'running', 'starttime':starttime, 'endtime':'N/A','snapshots':[]})
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

    def writeTestSnapshot(self,sid, tid, snapfile):
        """
        add snapshot png in image buffer
        """
        if self.mc:
            self.mc.set(sid+'snap', snapfile)

        if not (sid+'-'+tid) in self.imgBuffer:
            self.imgBuffer[sid+'-'+tid] = []
        try:
            idx = self.fs.put(snapfile)
            self.imgBuffer[sid+'-'+tid].append(str(idx))
            snapshots = self.imgBuffer[sid+'-'+tid] 
            caseresult = self.db['caseresult']
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
        for d in ret:
            snapids = d['snapshots'] 

        for fid in snapids:
            fs = self.getfile(fid)
            snaps.append(base64.encodestring(fs.read()))

        return {'snaps':snaps}

store = dbStore(server='192.168.7.212', port=27017)