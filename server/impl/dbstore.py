#!/usr/bin/env python

from pymongo import Connection
import gridfs
import mimetypes
import json
import datetime,time
import hashlib,uuid,base64
from bson.objectid import ObjectId

class snapshotNode(object):
    """
    Class snapBuffer maintain the frames of snapshot pngs to the test case
    """
    def __init__(self):
        self._frames = []

    def addFrame(self,rawdata):
        self._frames.append(rawdata)

    def clear(self):
        self._frames = []

    def getFrames(self):
        return self._frames

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
        m = hashlib.md5()
        m.update(password)
        ret = users.find({'appid':appid,'username':user,'password':m.hexdigest()})
        if not ret is None:
            for d in ret:
                uid = d['uid'] 
            tokens = self.db['token']
            token = str(uuid.uuid1())
            tokens.insert({'uid':uid,'token':token})
            return {'token':token}
        else:
            return {'code':1, 'msg':'user&password is not correct!'}

    def createTestSession(self,sid, planname, starttime, deviceid, devinfo):
        """
        write a test session record in database
        """
        session = self.db['session']
        session.insert({'sid':sid,
                       'planname':planname,
                       'result':{'total':0,'pass':0,'fail':0,'error':0},
                       'starttime':starttime,
                       'endtime': '', 
                       'runtime': 0,
                       'deviceid':deviceid,
                       'deviceinfo':devinfo
                      });

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
        caseresult = self.db['caseresult']
        rdata = caseresult.find({'sid':sid})
        result = {}
        lists = [{'tid':d['tid'],
                'sid':d['sid'],
                'casename':d['casename'],
                'starttime':d['starttime'],
                'endtime':d['endtime'],
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
                    'result':d['result'],
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
        self.imgBuffer[sid+'-'+tid] = snapshotNode()      
        caseresult = self.db['caseresult']
        caseresult.insert({'sid':sid, 'tid':tid, 'casename':casename, 'result':'running', 'starttime':starttime, 'endtime':starttime,'snapshots':[]})
        session = self.db['session']
        session.update({'sid':sid},{'$set':{'curCase':tid},'$inc':{'result.total':1}}) 

    def updateTestCaseResult(self, sid, tid, status):
        """
        update a test case resut record in database
        If case get failed, write snapshot png files in GridFS
        """
        caseresult = self.db['caseresult']
        session = self.db['session']
        status = status.lower()
        if status == 'pass' :
            session.update({'sid':sid},{'$inc':{'result.pass':1}})
        elif status == 'fail':
            session.update({'sid':sid},{'$inc':{'result.fail':1}})               
        else:
            session.update({'sid':sid},{'$inc':{'result.error':1}})

        caseresult.update({'sid':sid,'tid':tid},{'$set':{'result':status}})

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
        binfile =  open('./'+sid,'wb')
        binfile.write(snapfile)
        if not (sid+'-'+tid) in self.imgBuffer:
            self.imgBuffer[sid+'-'+tid] = snapshotNode()
        idx = self.fs.put(snapfile)
        self.imgBuffer[sid+'-'+tid].addFrame(str(idx))
 
        #session = self.db['session']
        #session.update({'sid':sid},{'$set':{'curFrame':str(idx)}}) 
        
        snapshots = self.imgBuffer[sid+'-'+tid].getFrames() 
        caseresult = self.db['caseresult']
        caseresult.update({'sid':sid,'tid':tid},{'$set':{'snapshots':snapshots}})

    def readTestLiveSnaps(self,sid):
        #session = self.db['session']
        #ret = session.find({'sid':sid})
        result = []
        #for d in ret:
        #    if 'curFrame' in d:
        #        fid = d['curFrame']
        #        ff = self.getfile(fid)
        #        result.append(ff)
        binfile = open('./'+sid,'rb')
        result.append(binfile.read())
        binfile.close()
        return result

    def readTestLiveResults(self,sid):
        session = self.db['session']
        caseresult = self.db['caseresult']   
        ret = session.find({'sid':sid})
        result = []
        for d in ret:
            if 'curCase' in d:
                tid = d['curCase']
                rr = caseresult.find({'tid':tid})
                for x in rr:
                    result.append('casename:%s, result:%s' % (x['casename'],x['result']))   
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