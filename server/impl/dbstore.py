#!/usr/bin/env python

#from pymongo import Connection
import gridfs
import memcache
import hashlib,uuid,base64
from bson.objectid import ObjectId
from datetime import datetime
import pymongo
from pymongo import ReplicaSetConnection
from pymongo.read_preferences import ReadPreference
from pymongo import ReadPreference
from pymongo.errors import AutoReconnect

class dbStore(object):
    """
    Class dbStore provides the access to MongoDB DataBase
    """
    def __init__(self, dbserver, dbport, mcserver, mcport):
        """
        do the database instance init works
        """
        print 'init db store class!!!'
        #self.db = Connection(dbserver, dbport)['smartServer']
        #self.fs = gridfs.GridFS(Connection(dbserver, dbport)['smartFiles'], collection='fs')
        conn = ReplicaSetConnection("192.168.5.60:27017,192.168.7.52:27017,192.168.7.210:27017", replicaSet='ats_rs')
        conn.read_preference = ReadPreference.SECONDARY_PREFERRED
        self.db = conn['smartServer']
        self.fs = gridfs.GridFS(conn['smartFiles'], collection='fs')
        connstr = '%s:%s' % (mcserver, mcport)
        self.mc = memcache.Client([connstr], debug=0)
        self.snapqueue = {}

    def counter(self, ctype):  
        ret = self.db.counter.find_and_modify(query={"_id":ctype},update={"$inc":{"next":1}},new=True,upsert=True)
        return int(ret["next"]); 

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

    def deletefile(self,fileId):
        '''
        Delete file.
        '''
        objId = ObjectId(fileId)
        self.fs.delete(objId)

    def createUser(self,appid,user,password,info):
        """
        write a user account record in database
        """
        uid = ''
        users = self.db['user']
        ret = users.find({'appid':appid,'username':user})
        for t in ret:
            uid = t['uid']

        if uid != '':
            return {'code':'04', 'msg':'An account with same username exists!'}            
        else:
            m = hashlib.md5()
            m.update(password)
            uid = '%05d' % self.counter('userid')
            users.insert({'uid':uid,'appid':appid,'username':user,'password':m.hexdigest(),'info':info})
            return {'uid':uid}

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
        _id = self.counter('sessionid')
        session = self.db['session']
        session.insert({'_id':_id,
                       'sid':sid,
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
        users = self.db['user']
        user = 'N/A'
        session = self.db['session']
        if uid == '00001':
            rdata = session.find()
        else:
            rdata = session.find({'uid':uid})
        result = {}
        dtnow = datetime.now()
        lists = []
        for d in rdata:
            if d['endtime'] == 'N/A':
                dttime = self.mc.get(str(d['sid'])+'timestamp')
                if dttime is None:
                    idletime = 1800 
                else:
                    idle = datetime.strptime(dttime, "%Y-%m-%d %H:%M:%S")
                    idletime = (dtnow - idle).seconds
                
                if idletime >= 1800:
                    d['endtime'] = 'Break'

            rrdata = users.find({'uid':d['uid']})
            for dd in rrdata:
                user = dd['username']

            lists.append({'_id':d['_id'],
                         'sid':d['sid'],
                         'user':user,
                         'planname':d['planname'],
                         'result':d['result'],
                         'starttime':d['starttime'],
                         'endtime':d['endtime'],
                         'runtime':d['runtime'],
                         'deviceid':d['deviceid'],
                         'deviceinfo':d['deviceinfo']})
        result['count'] = len(lists)
        result['sessions'] = lists
        return result

    def readTestSessionInfo(self,sid,uid):
        """
        read list of test session records in database
        """
        users = self.db['user']
        user = 'N/A'
        session = self.db['session']
        if uid == '00001':
            rdata = session.find({'sid':sid})
        else:
            rdata = session.find({'sid':sid, 'uid':uid})
        
        dtnow = datetime.now()
        for d in rdata:
            if d['endtime'] == 'N/A':
                dttime = self.mc.get(str(d['sid'])+'timestamp')
                if dttime is None:
                    idletime = 1800
                else:
                    idle = datetime.strptime(dttime, "%Y-%m-%d %H:%M:%S")
                    idletime = (dtnow - idle).seconds

                if idletime >= 1800:
                    d['endtime'] = 'Break'

            rrdata = users.find({'uid':d['uid']})
            for dd in rrdata:
                user = dd['username']

            result = {'_id':d['_id'],
                      'sid':d['sid'],
                      'user':user,
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
        self.snapqueue[sid+'-'+tid] = []
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.mc.set(sid+'timestamp',timestamp)
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
        runtime = 0
        snapshots = self.snapqueue[sid+'-'+tid]
        rdata = session.find({'sid':sid})
        for d in rdata:
            starttime = d['starttime']             
            d1 = datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S")
            d2 = datetime.strptime(endtime, "%Y-%m-%d %H:%M:%S")        
            runtime = (d2 - d1).seconds

        if status == 'pass':
            for d in snapshots:
                self.deletefile(d['fid'])
            snapshots = []
            session.update({'sid':sid},{'$inc':{'result.pass':1},'$set':{'runtime':runtime}})
        elif status == 'fail':
            session.update({'sid':sid},{'$inc':{'result.fail':1},'$set':{'runtime':runtime}})               
        else:
            session.update({'sid':sid},{'$inc':{'result.error':1},'$set':{'runtime':runtime}})

        caseresult.update({'sid':sid,'tid':tid},{'$set':{'result':status,'traceinfo':traceinfo,'endtime':endtime,'snapshots':snapshots}})

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

        if not (sid+'-'+tid) in self.snapqueue:
            self.snapqueue[sid+'-'+tid] = []
        try:
            idx = self.fs.put(snapfile)                
            fid = str(idx)
            caseresult = self.db['caseresult']
            posi = stype.index(':')
            sfiletype = stype[0:posi]
            sfile = stype[posi+1:]
            if sfiletype == 'expect':
                caseresult.update({'sid':sid,'tid':tid},{'$set':{'checksnap':{'title':sfile,'fid':fid} }})
            elif sfiletype == 'current':
                self.snapqueue[sid+'-'+tid].append({'title':sfile, 'fid':fid})
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
        stitle = ''
        for d in ret:
            snapids = d['snapshots']
            if not 'checksnap' in d:
                checkid = ''
                stitle = ''
            else:
                stitle = d['checksnap']['title']
                checkid = d['checksnap']['fid']
  
        if checkid != '':
            fs = self.getfile(checkid)
            if not fs is None:
                checksnap = {'title':stitle,'data': base64.encodestring(fs.read())}

        for d in snapids:
            stitle = d['title']
            fs = self.getfile(d['fid'])
            if not fs is None:
                snaps.append({'title':stitle,'data':base64.encodestring(fs.read())})   

        return {'snaps':snaps, 'checksnap':checksnap}

store = dbStore(dbserver='192.168.7.212', dbport=27017, mcserver='127.0.0.1',mcport='11211')
