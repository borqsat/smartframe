#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gridfs
import memcache
import hashlib
import uuid
import base64
from bson.objectid import ObjectId
from datetime import datetime
from datetime import timedelta
from collections import defaultdict
from random import choice
import string
import pymongo
from pymongo import MongoClient, MongoReplicaSetClient
from pymongo import ReadPreference

from ..config import MEMCACHED_URI, MONGODB_URI, MONGODB_REPLICASET
# TODO need refactoring
import beaker.cache
from beaker.util import parse_cache_config_options

mc_url = MEMCACHED_URI
cache = beaker.cache.Cache("memcached", type="ext:memcached",
                           lock_dir="/tmp/cache/lock",
                           url=mc_url, expire=600)
cache_opts = {
    'cache.lock_dir': '/tmp/cache/lock_memcached',
    'cache.type': 'ext:memcached',
    'cache.url': mc_url,
    'cache.expire': 600,
    'cache.regions': 'local, local_short',
    'cache.local_short.lock_dir': '/tmp/cache/lock_local_short',
    'cache.local_short.type': 'memory',
    'cache.local_short.expire': '10',
    'cache.local.lock_dir': '/tmp/cache/lock_local',
    'cache.local.type': 'memory',
    'cache.local.expire': '300'
}
cm = beaker.cache.CacheManager(**parse_cache_config_options(cache_opts))

DATE_FORMAT_STR = "%Y.%m.%d-%H.%M.%S"
DATE_FORMAT_STR1 = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT_STR2 = "%Y/%m/%d %H:%M"
IDLE_TIME_OUT = 1800


def _compareDateTime(dt1, dt2):
    date1 = datetime.strptime(dt1, DATE_FORMAT_STR)
    date2 = datetime.strptime(dt2, DATE_FORMAT_STR)
    return date1 > date2

def _deltaDataTime(dt1, dt2):
    delta = datetime.strptime(dt1, DATE_FORMAT_STR) - datetime.strptime(dt2, DATE_FORMAT_STR)
    return delta.days * 86400 + delta.seconds

class DataStore(object):

    """
    Class DbStore provides the access to MongoDB DataBase
    """

    def __init__(self, mongo_client, mem):
        """
        do the database instance init works
        """
        print 'init db store class!!!'

        self._db = mongo_client.smartServer
        self._fsdb = mongo_client.smartFiles
        self._fs = gridfs.GridFS(self._fsdb, collection="fs")
        self._mc = mem

    def counter(self, keyname):
        ret = self._db.counter.find_and_modify(query={
                                               "_id": keyname}, update={"$inc": {"next": 1}}, new=True, upsert=True)
        return int(ret["next"])

    def convert_to_datetime(self, time_str):
        '''convert a string to datetime or None in case of invalid string'''
        dt = None
        try:
            dt = datetime.strptime(time_str, DATE_FORMAT_STR)
        except:
            pass
        if dt is None:
            try:
                dt = datetime.strptime(time_str, DATE_FORMAT_STR1)
            except:
                pass
        return dt

    def convert_to_str(self, date):
        '''convert a datetime to formatted string.'''
        # TODO Why to use the format...
        return date.strftime(DATE_FORMAT_STR)

    def validate_session_endtime(self):
        '''
        If a "N/A" session has not been updated for 60mins, set a reasonable endtime to it,
        if this is a dirty session, which has session info but no related cases, ignore it here.
        '''
        print "Start to validate session endtime"
        for session in self._db['testsessions'].find({'endtime': 'N/A'}, {'sid': 1, 'starttime': 1}):
            cases_collection = self._db['testresults'].find({'sid': session['sid']}, {
                                                            'starttime': 1, 'endtime': 1}).sort('starttime', pymongo.DESCENDING)
            if cases_collection.count() == 0:
                endtime = self.convert_to_datetime(session['starttime'])
            else:
                case = cases_collection[0]
                endtime = self.convert_to_datetime(
                    case['starttime'] if case['endtime'] is 'N/A' else case['endtime'])

            if endtime is not None and (datetime.now() - endtime).total_seconds() >= 3600:
                # TODO: Should use time of database server as "now" time
                self._db['testsessions'].update(
                    {'sid': session['sid']}, {'$set': {'endtime': self.convert_to_str(endtime)}})

    def active_testsession(self, sid):
        '''Set session endtime to "N/A", back to life'''
        print "Start to active testsession"
        self._db['testsessions'].update(
            {'sid': sid}, {'$set': {'endtime': 'N/A'}})

    def validate_testcase_endtime(self):
        '''
        If a testcase has not been updated for 60 mins, set its starttime as its endtime,
        if this is a dirty case, which does not even have reasonable starttime, remove it
        '''
        print "Start to validate testcase endtime"
        for case in self._db['testresults'].find({'endtime': 'N/A', 'result': 'running'}, {'starttime': 1, 'sid': 1}):
            starttime = self.convert_to_datetime(case['starttime'])
            if starttime is None:
                self._db['testresults'].remove({'_id': case['_id']})
                self.updateTestsessionSummary(case['sid'])
            elif (datetime.now() - starttime).total_seconds() >= 3600:
                # TODO: Should use time of database server as "now" time
                self._db['testresults'].update({'_id': case['_id']},
                                               {'$set': {'endtime': self.convert_to_str(starttime),
                                                         'result': 'error',
                                                         'traceinfo': 'No results uploaded in 60mins, set it ERROR'}})
                self.updateTestsessionSummary(case['sid'])

    def del_testcase(self, tid):
        self._db['testresults'].remove({'_id': tid})

    def del_session(self, sid):
        '''
        Clear test results and the relative files including snapshots,
        checksnap and log files according to the sid.
        By zsf
        '''
        r_collection = self._db['testresults']
        # get all the result of the sid
        trs = r_collection.find(spec={'sid': sid},
                                fields={'snapshots': True, 'checksnap': True, 'log': True, '_id': False})

        fids = set()
        for record in trs:
            if 'snapshots' in record:
                for snap in record['snapshots']:
                    fids.add(snap['fid'])

            if 'checksnap' in record:
                fids.add(record['checksnap']['fid'])

            if 'log' in record:
                fids.add(record['log'])

        # TODO: Improve the speeed of deletion
        if 'N/A' in fids:
            fids.remove('N/A')

        print 'Begin to delete all the files relative the session: %s' % sid
        for f in fids:
            self.deletefile(f)

        # remove test result
        print 'Begin to delete all the test results relative the session: %s' % sid
        r_collection.remove({'sid': sid})

    def del_group(self, gid):
        '''
        Clear all test results and relative files belong to the gid
        By zsf
        '''
        s_collection = self._db['testsessions']

        # get all sessions of gid
        ss = s_collection.find(spec={'gid': gid},
                               fields={'sid': True, '_id': False})

        # delete all data relative all sid
        print "Begin to delete all the session data relative the group: %s" % gid
        for s in ss:
            self.del_session(s['sid'])

        # remove all sessions
        s_collection.remove({'gid': gid})

    def _del_dirty_testsession(self):
        '''
        Delete all sessions which gid is not in groups collection
        By zsf
        '''
        s_collection = self._db['testsessions']
        g_collection = self._db['groups']

        g_sset = set()
        g_gset = set()

        print 'Begin to find the dirty sid...' + datetime.now().strftime(DATE_FORMAT_STR1)

        # get all gids from test session
        for s in s_collection.find(fields={'gid': True}):
            g_sset.add(s['gid'])

        # get all gids from groups
        for g in g_collection.find(fields={'gid': True}):
            g_gset.add(g['gid'])

        # delete all sessions which gid is not in groups
        print 'Begin to clear dirty sessions...' + datetime.now().strftime(DATE_FORMAT_STR1)
        for t in g_sset - g_gset:
            s_collection.remove({'gid': t})
        print 'Finish to clear dirty sessions...' + datetime.now().strftime(DATE_FORMAT_STR1)

    def _del_dirty_testresult(self):
        '''
        Delete all test result which sid is not in test session collection
        '''
        r_collection = self._db['testresults']
        s_collection = self._db['testsessions']

        s_sset = set()
        s_rset = set()

        print 'Begin to find the dirty result...' + datetime.now().strftime(DATE_FORMAT_STR1)
        # get all sids from test session
        for s in s_collection.find(fields={'sid': True}):
            s_sset.add(s['sid'])

        # get all sids from test results
        for r in r_collection.find(fields={'sid': True}):
            s_rset.add(r['sid'])

        # delete all test results which sid is not in test session
        print 'Begin to clear dirty test results... ' + datetime.now().strftime(DATE_FORMAT_STR1)
        for t in s_rset - s_sset:
            r_collection.remove({'sid': t})
        print 'Finish to clear dirty test results... ' + datetime.now().strftime(DATE_FORMAT_STR1)

    def _del_dirty_fs(self):
        '''
        Delete all fs which test results has been deleted.
        '''
        fs_collection = self._fsdb['fs.files']
        r_collection = self._db['testresults']

        fid_aset = set()
        fid_rset = set()

        print 'Begin to find dirty fs... ' + datetime.now().strftime(DATE_FORMAT_STR1)
        # Only consider files, created 3 days ago, could be dirty files
        for f in fs_collection.find(
            spec={'uploadDate': {'$lt': datetime.now() - timedelta(3)}},
                fields={'_id': True}):
            fid_aset.add(str(f['_id']))

        trs = r_collection.find(
            spec={'$or': [{'result': 'fail'}, {'result': 'error'}]},
            fields={'snapshots': True, 'checksnap': True, 'log': True})
        for record in trs:
            if 'snapshots' in record and record['snapshots'] is not None:
                for snap in record['snapshots']:
                    fid_rset.add(snap['fid'])

            if 'checksnap' in record and record['checksnap'] is not None:
                fid_rset.add(record['checksnap']['fid'])

            if 'log' in record:
                fid_rset.add(record['log'])

        tmp_set = fid_aset - fid_rset
        if 'N/A' in tmp_set:
            tmp_set.remove('N/A')
            print 'NA is in dirty fs...'

        print 'Begin to clear dirty files. Total: %d' % len(tmp_set)
        print datetime.now().strftime(DATE_FORMAT_STR1)
        for tmp_fid in tmp_set:
            self.deletefile(tmp_fid)
        print 'Finish to clear dirty files...' + datetime.now().strftime(DATE_FORMAT_STR1)

    def del_dirty(self):
        '''
        '''
        self._del_dirty_testsession()
        self._del_dirty_testresult()
        self._del_dirty_fs()

    def check_fs(self, fid):
        r_collection = self._db['testresults']

        flag_snap = False
        flag_check = False
        flag_log = False

        trs = r_collection.find(fields={
                                'checksnap': True, 'log': True, 'snapshots': True})
        for record in trs:
            if 'checksnap' in record:
                if fid == record['checksnap']['fid']:
                    flag_check = True

            if 'log' in record:
                if fid == record['log']:
                    flag_log = True

            if 'snapshots' in record:
                for snap in record['snapshots']:
                    if fid == snap['fid']:
                        flag_snap = True
                        break

        print 'Flag_log: ' + str(flag_log)
        print 'Flag_snap: ' + str(flag_snap)
        print 'Flag_check: ' + str(flag_check)

        return [flag_log, flag_snap, flag_check]

    def getfile(self, fileId):
        '''
        Get file.
        '''
        data = None
        objId = ObjectId(fileId)
        exists = self._fs.exists(objId)
        if exists:
            data = self._fs.get(objId)
        return data

    def setfile(self, data):
        '''
        Get file.
        '''
        fid = self._fs.put(data)
        return str(fid)

    def deletefile(self, fileId):
        '''
        Delete file.
        '''
        objId = ObjectId(fileId)
        self._fs.delete(objId)

    def setCache(self, key, value=None):
        '''
        set Cache value.
        '''
        if not self._mc is None:
            self._mc.set(key, value)
            return key
        else:
            return None

    def getCache(self, key):
        '''
        get Cache value.
        '''
        if not self._mc is None:
            value = self._mc.get(key)
            return value
        else:
            return None

    def clearCache(self, key):
        '''
        get Cache value.
        '''
        if not self._mc is None:
            self._mc.delete(key)

    def createUser(self, appid, user, password, info):
        """
        write a user account record in database
        """
        uid = ''
        users = self._db['users']
        tokens = self._db['tokens']
        ret = users.find_one({'username': user})
        if not ret is None:
            return {'code': '04', 'msg': 'An account with same username already registered!'}

        ret = users.find_one({'info.email': info['email']})
        if not ret is None:
            return {'code': '04', 'msg': 'An account with same email already registered!'}

        m = hashlib.md5()
        m.update(password)
        pswd = m.hexdigest()
        m.update('%08d' % self.counter('userid'))
        uid = m.hexdigest()
        users.insert({'uid': uid, 'appid': appid, 'username':
                     user, 'password': pswd, 'active': False, 'info': info})
        return {'uid': uid}

    def createGroup(self, groupname, info):
        """
        write a user account record in database
        """
        gid = ''
        groups = self._db['groups']
        ret = groups.find({'groupname': groupname})
        for d in ret:
            gid = d['gid']

        if gid != '':
            return {'code': '04', 'msg': 'A group with same username exists!'}
        else:
            m = hashlib.md5()
            m.update('%08d' % self.counter('groupid'))
            gid = m.hexdigest()
            groups.insert({'gid': gid, 'groupname': groupname, 'info': info})
            return {'gid': gid}

    def deleteGroup(self, gid, uid):
        '''
        Delete a group and it's data
        TODO: Maybe a bug: role only exists in group_members?
        '''
        group = self._db['groups'].find_one({'gid': gid})
        if group is None:
            return {'errors': {'code': 0, 'msg': 'Invalid group.'}}

        collections = ['groups', 'group_members']
        for collec in collections:
            self._db[collec].remove({'gid': gid})
        return {'results': 1}

    def addGroupMember(self, gid, uid, role):
        members = self._db['group_members']
        vrole = None
        ret = members.find({'gid': gid, 'uid': uid})
        for d in ret:
            vrole = d['role']

        if not vrole is None:
            members.update({'gid': gid, 'uid': uid}, {'$set': {'role': role}})
        else:
            members.insert({'gid': gid, 'uid': uid, 'role': role})
        return {'gid': gid}

    def setGroupMember(self, gid, uid, role):
        members = self._db['group_members']
        members.update({'gid': gid, 'uid': uid}, {'$set': {'role': role}})
        return {'gid': gid}

    def delGroupMember(self, gid, uid):
        members = self._db['group_members']
        members.remove({'gid': gid, 'uid': uid})
        return {'gid': gid}

    def getUserRole(self, gid, uid):
        members = self._db['group_members']
        retdata = members.find({'gid': gid, 'uid': uid})
        result = {}
        for d in retdata:
            result = {'uid': d['uid'], 'role': d['role']}
        return result

    def getGroupInfo(self, gid, with_members=True):
        '''
        Get the group info with its members info.
        Return None in case of the gid does not exist.
        '''
        group = self._db['groups'].find_one({'gid': gid})
        if group is None:  # return None in case of not exist
            return None

        if with_members:
            group_members = self._db['group_members']
            group["members"] = [{'uid': m['uid'],
                                 'username': self.userInfo(m['uid'], False, False)['username'],
                                 'role': m['role']}
                                for m in group_members.find({'gid': gid})
                                if self.userInfo(m['uid'], False, False) is not None]  # workaround. Why there are some data with invalid uid?
        del group["_id"]
        return group

    @cm.region("local_short", "group_info")
    def groupInfo(self, gid, with_members):
        ''' Cache the result of getGroupInfo method'''
        return self.getGroupInfo(gid, with_members)

    def getUserInfo(self, uid, with_group=True, with_test=True):
        '''
        Get the user ino with its groups info and test sessions info.
        Return None in case of the uid does not exist.
        '''
        user = self._db['users'].find_one({'uid': uid})
        if user is None:  # return None in case of not exist
            return None

        result = {'uid': uid, 'username': user['username'], 'info': user['info']}

        if with_group:
            members = self._db['group_members']
            result['inGroups'] = [{'gid': m['gid'],
                                   'role': m['role'],
                                   'groupname': self.groupInfo(m['gid'], False)['groupname']}
                                  for m in members.find({'uid': uid})
                                  if self.groupInfo(m['gid'], False) is not None]  # workaround. Why there are some data with invalid gid?

        if with_test:
            sessions = self._db['testsessions']
            result['inTests'] = [{'sessionid': s['id'],
                                  'sid': s['sid'],
                                  'groupname': self.groupInfo(s['gid'], False)['groupname'],
                                  'gid': s['gid']}
                                 for s in sessions.find({'tester': uid})
                                 if self.groupInfo(s['gid'], False) is not None]  # workaround. Why there are some data with invalid gid?

        return result

    @cm.region("local_short", "user_info")
    def userInfo(self, uid, with_group, with_test):
        ''''Cached the result of getUserInfo method'''
        return self.getUserInfo(uid, with_group, with_test)

    def userChangePassword(self, uid, oldpassword, newpassword):
        m = hashlib.md5()
        m.update(oldpassword)
        users = self._db['users']
        rdata = users.find_one({'uid': uid})
        if m.hexdigest() == rdata['password']:
            m = hashlib.md5()
            m.update(newpassword)
            users.update({'uid': uid}, {'$set': {'password': m.hexdigest()}})
            return {'uid': uid}
        else:
            return {'code': '03', 'msg': 'Incorrect original password!'}

    def userUpdateInfo(self, uid, info):
        users = self._db['users']
        data = {}
        results = {}
        results['uid'] = uid
        if 'email' in info:
            rdata = users.find_one({'info.email': info['email']})
            if rdata is not None:
                return {'code': '05', 'msg': 'Email already bound with an existed account!'} 
            rdata = users.find_one({'uid': uid})
            results['email'] = info['email']
            results['username'] = rdata['username']
            data['active'] = False

        for key in info:
            data['info.%s' % key] = info[key]
        users.update({'uid': uid}, {'$set': data})
        return results

    def userExists(self, username, password):
        users = self._db['users']
        if '@' in username:
            rdata = users.find_one({
                                   'info.email': username, 'password': password, 'active': True})
        else:
            rdata = users.find_one({
                                   'username': username, 'password': password})
        if not rdata is None:
            return rdata['uid']
        else:
            return None
            
    def findUserByEmail(self, email):
        users = self._db['users']
        if '@' in email:
            rdata = users.find_one({
                                   'info.email': email, 'active': True})
        if not rdata is None:
            newpassword = ''.join([choice(string.ascii_letters+string.digits) for i in range(8)])
            m = hashlib.md5()
            m.update(newpassword)
            users.update({'uid': rdata['uid']}, {'$set': {'password': m.hexdigest()}})
            return {'uid':rdata['uid'],'password':newpassword}
        else:
            return None

    def activeUser(self, uid):
        users = self._db['users']
        users.update({'uid': uid}, {'$set': {'active': True}})
        return {'uid': uid}

    def getUserList(self):
        results = {}
        lists = []
        users = self._db['users']
        rdata = users.find()
        lists = [{'uid': d['uid'], 'username':d['username']} for d in rdata]
        results['count'] = len(lists)
        results['users'] = lists
        return results

    # TODO cache policy...
    @cm.region("local", "user_id")
    def validToken(self, token):
        uid = ''
        username = ''
        tokens = self._db['tokens']
        rdata = tokens.find({'token': token})
        for t in rdata:
            uid = t['uid']

        if uid != '':
            users = self._db['users']
            rdata = users.find_one({'uid': uid})
            if not rdata is None:
                username = rdata['username']
            return {'uid': uid, 'username': username}
        else:
            return {'code': '02', 'msg': 'Invalid token!'}

    def createToken(self, appid, uid, info, expires):
        """
        write a user account record in database
        """
        tokens = self._db['tokens']
        m = hashlib.md5()
        m.update(str(uuid.uuid1()))
        token = m.hexdigest()
        tokens.insert({'appid': appid, 'uid': uid,
                      'info': info, 'token': token, 'expires': expires})
        return {'token': token, 'uid': uid}

    def deleteToken(self, token):
        tokens = self._db['tokens']
        tokens.remove({'token': token})

    def createTestSession(self, gid, sid, uid, value):
        """
        write a test session record in database
        """
        vid = self.counter('group' + gid)
        sessions = self._db['testsessions']
        deviceid = value['deviceid']
        if deviceid is None:
            deviceid = 'N/A'
        sessions.insert({'id': vid, 'gid': gid, 'sid': sid,
                         'tester': uid, 'planname': value['planname'],
                         'starttime': value['starttime'], 'endtime': 'N/A', 'runtime': 0,
                         'summary': {'total': 0, 'pass': 0, 'fail': 0, 'error': 0},
                         'deviceid': deviceid, 'deviceinfo': value['deviceinfo']})

    def updateTestSession(self, gid, sid, value):
        """
        write a test session record in database
        """
        result = {}
        session = self._db['testsessions']
        if 'cid' in value:
            cid = value['cid']
            if cid < 0:
                cid = ''
            elif cid == 0:
                cid = self.counter('cid')

            result['cid'] = cid

        if 'endtime' in value:
            result['endtime'] = value['endtime']
            self.clearCache(str('sid:' + sid + ':snap'))
            self.clearCache(str('sid:' + sid + ':snaptime'))

        session.update({'gid': gid, 'sid': sid}, {'$set': result})

    def deleteTestSession(self, gid, sid):
        """
        delete a test session from database
        """
        session = self._db['testsessions']
        session.remove({'gid': gid, 'sid': sid})

    @cm.region("local_short", "session_time")
    def getSessionLasttime(self, sid):
        tResult = self._db['testresults']
        result = 'N/A'
        specs = {'sid': sid}
        ret = tResult.find(spec=specs, limit=1, sort=[('tid', pymongo.DESCENDING)])
        for line in ret:
            result = line['starttime']
        return result

    def getSessionTime(self, sid):
        """
        get last update of a test session
        """
        idletime = 0
        dtnow = datetime.now().strftime(DATE_FORMAT_STR)
        dttime = self.getCache(str('sid:' + sid + ':uptime'))
        if dttime is not None:
            idletime = _deltaDataTime(dtnow, dttime)
        else:
            idletime = IDLE_TIME_OUT

        result = self.getSessionLasttime(sid) if idletime >= IDLE_TIME_OUT else 'N/A'
        return result

    def readTestSessionList(self, gid):
        """
        read list of test session records in database
        """
        users, session = self._db['users'], self._db['testsessions']
        rdata = session.find({'gid': gid})
        result = {}
        for d in rdata:
            if d['endtime'] == 'N/A':
                d['endtime'] = self.getSessionTime(d['sid'])

            d['status'] = 'running' if d['endtime'] == 'N/A' else 'end'
            user = self.userInfo(d['tester'], False, False)["username"]
            cid = d.get('cid', '')
            if cid not in result:
                result.setdefault(cid, {'cid': cid,
                                        'count': 0,
                                        'livecount': 0,
                                        'starttime': '--',
                                        'endtime': '--',
                                        'product': '--',
                                        'sessions': []})

            current = result.get(cid)
            current['count'] += 1
            current['product'] = d['deviceinfo'].get('product', '--')

            if current['starttime'] == '--' or _compareDateTime(current['starttime'], d['starttime']):
                current['starttime'] = d['starttime']

            if current['endtime'] != 'N/A':
                if current['endtime'] == '--' or d['endtime'] == 'N/A' or _compareDateTime(d['endtime'], current['endtime']):
                    current['endtime'] = d['endtime']

            if d['endtime'] == 'N/A':
                current['livecount'] += 1

            current['sessions'].append({'id': d['id'],
                                        'sid': d['sid'],
                                        'gid': d['gid'],
                                        'tester': user,
                                        'starttime': d['starttime'],
                                        'endtime': d['endtime'],
                                        'status': d['status'],
                                        'runtime': d['runtime'],
                                        'deviceid': d['deviceid'],
                                        'revision': d['deviceinfo'].get('revision', '--')})

        return {'results': result.values()}

    def readTestReport(self, gid, cid):
        """
        give a cycle report data
        """
        session = self._db['testsessions']
        caseresult = self._db['testresults']
        sidList = []
        res1 = {'product': '--',
                'count': 0,
                'starttime':'--',
                'endtime':'--',
                'failcnt':0,
                'totaldur':0
                }
        res2 = []
        res3 = []
        res4 = []
        rdata = session.find({'gid': gid, 'cid': int(cid)})
        for d in rdata:
            sidList.append(d['sid'])
            if 'failtime' in d:
                d['endtime'] = d['failtime']

            res1['product'] = d['deviceinfo']['product']
            res1['buildid'] = d['deviceinfo']['revision']
            res1['count'] += 1
            if res1['starttime'] == '--' or _compareDateTime(res1['starttime'], d['starttime']):
                res1['starttime'] = d['starttime']

            if res1['endtime'] != 'N/A':
                if res1['endtime'] == '--' or d['endtime'] == 'N/A' or _compareDateTime(d['endtime'], res1['endtime']):
                    res1['endtime'] = d['endtime']

            tmpEndTime = (d['endtime'] == 'N/A' and self.getSessionLasttime(d['sid'])) or d['endtime']
            tmpDur = _deltaDataTime(tmpEndTime, d['starttime'])
            res1['totaldur'] += tmpDur
            tmpR3 = {}
            tmpR3['imei'] = d['deviceid']
            tmpR3['sid'] = d['sid']
            tmpR3['starttime'] = datetime.strftime(datetime.strptime(
                d['starttime'], DATE_FORMAT_STR), DATE_FORMAT_STR2)
            tmpR3['endtime'] = (d['endtime'] == 'N/A') and d['endtime'] or datetime.strftime(
                datetime.strptime(d['endtime'], DATE_FORMAT_STR), DATE_FORMAT_STR2)
            tmpR3['failcount'] = 0
            tmpR3['totaldur'] = tmpDur
            tmpR3['caselist'] = []
            tmpFailTime = tmpEndTime
            
            blockDur = 0
            fblockDur = 0
            tmpBlockStart = ''
            tmpBlockEnd = ''
            lastTid = 0
            rdata3 = caseresult.find({'sid': d['sid'],'comments.caseresult': {'$in': ['fail', 'Fail', 'block', 'Block']}}).sort('tid',pymongo.ASCENDING)
            for d3 in rdata3:
                if d3['comments']['caseresult'] == 'block' or d3['comments']['caseresult'] == 'Block':
                    if d3['tid']!=lastTid+1 and lastTid!=0:
                        blockDur+=_deltaDataTime(tmpBlockEnd,tmpBlockStart)
                        tmpBlockStart = ''
                        tmpBlockEnd = ''
                    if tmpBlockEnd == '' or d3['tid']==lastTid+1: 
                        tmpBlockEnd=d3['endtime']
                    if tmpBlockStart == '': 
                        tmpBlockStart=d3['starttime']
                    lastTid = d3['tid']
                    
                if d3['comments']['caseresult'] == 'fail' or d3['comments']['caseresult'] == 'Fail':
                    if _compareDateTime(tmpFailTime, d3['starttime']): 
                        tmpFailTime = d3['starttime']
                        fblockDur = blockDur -1 + ((tmpBlockStart=='' or tmpBlockEnd=='') and 1 or _deltaDataTime(tmpBlockEnd,tmpBlockStart)+1)    
                    tmpR3['caselist'].append({'happentime': datetime.strftime(datetime.strptime(d3['starttime'], DATE_FORMAT_STR), DATE_FORMAT_STR2), 
                                         'issuetype': d3['comments']['issuetype'], 
                                         'comments': d3['comments']['commentinfo']})
                    res1['failcnt'] += 1
                    tmpR3['failcount'] += 1
                if 'comments.endsession' in d3 and d3['comments']['endsession']==1: break 

            if tmpBlockStart!='':
                blockDur+=_deltaDataTime(tmpBlockEnd,tmpBlockStart)
            res1['totaldur']-=blockDur
            tmpR3['totaldur']-=blockDur

            if rdata3.count() <= 0:
                tmpR3['faildur'] = 0
            else:
                tmpR3['faildur'] = _deltaDataTime(tmpFailTime, d['starttime']) - fblockDur
            res3.append(tmpR3)

        rdata2 = caseresult.group({'comments.issuetype': 1}, {'sid': {'$in': sidList}, 'comments.caseresult': {
            '$in': ['fail', 'Fail']}}, {'cnt': 0}, 'function(obj,prev) { prev.cnt+=1; }')
        for d in rdata2:
            res2.append(
                {'issuetype': d['comments.issuetype'], 'count': d['cnt']})

        rdata4 = caseresult.group({'casename': 1}, {'sid': {'$in': sidList}}, {'totalcnt': 0, 'passcnt': 0, 'failcnt': 0, 'blockcnt': 0}, '''
          function(obj,prev){
            prev.totalcnt+=1;
            if(obj.result=='pass'){
                prev.passcnt+=1;
            }else if('comments' in obj && obj.comments.caseresult !== undefined) {
                var resulttag = obj.comments.caseresult.toLowerCase();
                if (resulttag == 'fail') { prev.failcnt+=1; }
                else if (resulttag == 'block') { prev.blockcnt+=1; }
            }
          }
          ''')
        domainTag = {}
        tmpi = 0

        for d in rdata4:
            try:
                tmpDomain = d['casename'].split('.')[-2]
            except:
                continue
            if tmpDomain not in domainTag:
                domainTag[tmpDomain] = tmpi
                tmpi += 1
                res4.append(
                    {'domain': tmpDomain, 'totalcnt': 0, 'passcnt': 0, 'failcnt': 0, 'blockcnt': 0, 'detail': []})
            tmpj = domainTag[tmpDomain]
            res4[tmpj]['passcnt'] += d['passcnt']
            res4[tmpj]['failcnt'] += d['failcnt']
            res4[tmpj]['blockcnt'] += d['blockcnt']
            tmpTotal = d['passcnt'] + d['failcnt'] + d['blockcnt']
            res4[tmpj]['totalcnt'] += tmpTotal
            res4[tmpj]['detail'].append(
                {'casename': d['casename'], 'totalcnt': tmpTotal, 'passcnt': d['passcnt'], 'failcnt': d['failcnt'], 'blockcnt': d['blockcnt']})

        res1['starttime'] = datetime.strftime(datetime.strptime(res1['starttime'], DATE_FORMAT_STR), DATE_FORMAT_STR2)
        if res1['endtime'] != 'N/A':
            res1['endtime'] = datetime.strftime(datetime.strptime(res1['endtime'], DATE_FORMAT_STR), DATE_FORMAT_STR2)

        result = {}
        result['cylesummany'] = res1
        result['issuesummany'] = res2
        result['issuedetail'] = res3
        result['domain'] = res4
        return result

    def readTestSessionInfo(self, gid, sid):
        """
        read list of test session records in database
        """
        users = self._db['users']
        user = 'N/A'
        session = self._db['testsessions']
        d = session.find_one({'gid': gid, 'sid': sid})

        dtnow = datetime.now()
        if d is not None:
            if d['endtime'] == 'N/A':
                d['endtime'] = self.getSessionTime(d['sid'])

            dd = users.find_one({'uid': d['tester']})
            if dd is not None:
                user = dd['username']

            result = {'id': d['id'],
                      'gid': d['gid'],
                      'sid': d['sid'],
                      'tester': user,
                      'planname': d['planname'],
                      'starttime': d['starttime'],
                      'endtime': d['endtime'],
                      'runtime': d['runtime'],
                      'summary': d['summary'],
                      'deviceid': d['deviceid'],
                      'deviceinfo': d['deviceinfo']}

        caseresult = self._db['testresults']
        rdata = caseresult.find({'sid': sid})
        lists = [{'tid': d['tid'],
                  'casename':d['casename'],
                  'starttime':d['starttime'],
                  'endtime':d['endtime'],
                  'traceinfo':d['traceinfo'],
                  'result':d['result']} for d in rdata]
        result['count'] = len(lists)
        result['cases'] = lists
        return result

    def isSessionUpdated(self, gid, sid, tid):
        tResult = self._db['testresults']
        record = tResult.find_one({
                                  'gid': gid, 'sid': sid, 'tid': {'$gt': int(tid)}})
        if record is None:
            return 0
        else:
            return 1

    def getSessionLiveCases(self, gid, sid, maxCount):
        tSession = self._db['testsessions']
        ret = tSession.find_one({'sid': sid})
        summary = {}
        runtime = 0
        if ret is None:
            summary['total'] = 0
            summary['pass'] = 0
            summary['fail'] = 0
            summary['error'] = 0
        else:
            summary = ret['summary']
            runtime = ret['runtime']

        tResult = self._db['testresults']
        specs = {'gid': gid, 'sid': sid}
        fields = {'_id': False, 'gid': False, 'sid': False,
                  'log': False, 'checksnap': False, 'snapshots': False}
        records = tResult.find(spec=specs, fields=fields,
                               limit=int(maxCount), sort=[('tid', pymongo.DESCENDING)])
        cases = []
        for record in records:
            cases.append(record)

        result = {}
        result['runtime'] = runtime
        result['summary'] = summary
        result['cases'] = cases
        return result

    def getSessionAllCases(self, gid, sid, type='total', page=1, pagesize=100):
        tSession = self._db['testsessions']
        ret = tSession.find_one({'sid': sid})
        if ret is None:
            return None
        result = {}
        paging = {}
        total = 0
        if type in ret['summary']:
            total = ret['summary'][type]
        else:
            return None
        if (total % pagesize != 0):
            paging['totalpage'] = (total / pagesize + 1)
        else:
            paging['totalpage'] = (total / pagesize)
        paging['curpage'] = page
        paging['pagesize'] = pagesize

        tResult = self._db['testresults']
        if type == 'total':
            specs = {'sid': sid}
        else:
            specs = {'sid': sid, 'result': type}
        fields = {'_id': False, 'gid': False, 'sid': False}
        records = tResult.find(
            spec=specs, fields=fields, skip=int((page - 1) * pagesize),
            limit=int(pagesize), sort=[('tid', pymongo.DESCENDING)])
        cases = []
        for record in records:
            cases.append(record)

        result['count'] = len(cases)
        result['paging'] = paging
        result['cases'] = cases
        return result

    def getSessionSummary(self, gid, sid):
        tSession = self._db['testsessions']
        d = tSession.find_one({'sid': sid})
        if d is None:
            return None

        if d['endtime'] == 'N/A':
            d['endtime'] = self.getSessionTime(d['sid'])

        if 'tester' in d:
            users = self._db['users']
            u = users.find_one({'uid': d['tester']})
            if not u is None:
                d['tester'] = u['username']
        d.pop('_id')
        return d

    def readTestCaseInfo(self, gid, sid, tid):
        """
        read list of test cases records in database
        """
        caseresult = self._db['testresults']
        result = None
        ret = caseresult.find_one({'sid': sid, 'tid': int(tid)})
        if not ret is None:
            result = {'tid': ret['tid'],
                      'casename': ret['casename'],
                      'starttime': ret['starttime'],
                      'endtime': ret['endtime'],
                      'result': ret['result'],
                      'traceinfo': ret['traceinfo'],
                      'log': ret['log'],
                      'snapshots': ret['snapshots'],
                      'checksnap': ret['checksnap']}
        return result

    def createTestCaseResult(self, gid, sid, tid, casename, starttime):
        """
        write a test case result record in database
        """
        self.setCache(str('sid:' + sid + ':tid:' + tid + ':snaps'), [])
        timestamp = datetime.now().strftime(DATE_FORMAT_STR)
        self.setCache(str('sid:' + sid + ':uptime'), timestamp)
        caseresult = self._db['testresults']
        caseresult.insert({'gid': gid, 'sid': sid, 'tid': int(tid),
                           'casename': casename, 'log': 'N/A', 'starttime': starttime, 'endtime': 'N/A',
                           'traceinfo': 'N/A', 'result': 'running',  'snapshots': []})

    def updateTestcaseComments(self, gid, sid, tid, results):
        caseresult = self._db['testresults']
        comments = results['comments']

        tids = []
        for tmp in comments.pop('tids'):
            tids.append(int(tmp))

        if comments['endsession'] == 1:
            tmpt = caseresult.find_one({'gid': gid, 'sid': sid, 'tid': tids[0]}, {'endtime': 1, '_id': 0})
            self._db['testsessions'].update({'gid': gid, 'sid': sid}, {'$set': {'failtime': tmpt['endtime']}})

        return caseresult.update({'gid': gid, 'sid': sid, 'tid': {'$in': tids}}, {'$set': {'comments': comments}}, multi=True)

    def updateTestsessionSummary(self, sid):
        '''
        count the pass/fail/error cases of a session,
        calculate the runtime of a session
        '''
        #TODO: This func. can be optimized.

        passCount = store._db['testresults'].find({'sid': sid, 'result': 'pass'}).count()
        failCount = store._db['testresults'].find({'sid': sid, 'result': 'fail'}).count()
        errorCount = store._db['testresults'].find({'sid': sid, 'result': 'error'}).count()
        total = store._db['testresults'].find({'sid': sid}, {'result': 1}).count()

        tids = self._db['testresults'].find({'sid': sid}, {'_id': 0, 'tid': 1}).distinct('tid')
        minStartTime = self.convert_to_datetime(store._db['testresults'].find_one({'sid': sid, 'tid': tids[-1]}, {'starttime': 1})['starttime'])
        case = store._db['testresults'].find_one({'sid': sid, 'tid': tids[0]}, {'starttime': 1, 'endtime': 1})
        maxEndTime = self.convert_to_datetime(case['starttime'] if case['endtime'] == 'N/A' else case['endtime'])

        if maxEndTime and minStartTime:
            runtime = (maxEndTime - minStartTime).total_seconds()
        else:
            runtime = 0

        self._db['testsessions'].update({'sid': sid},
                                        {'$set': {'summary.pass': passCount,
                                                  'summary.fail': failCount,
                                                  'summary.error': errorCount,
                                                  'runtime': runtime,
                                                  'summary.total': total}})

    def updateTestCaseResult(self, gid, sid, tid, results):

        if tid == '00000':
            return self.updateTestcaseComments(gid, sid, tid, results)

        self.setCache(str('sid:' + sid + ':uptime'),
                      datetime.now().strftime(DATE_FORMAT_STR))
        snapshots = self.getCache(str('sid:' + sid + ':tid:' + tid + ':snaps'))
        self.clearCache(str('sid:' + sid + ':tid:' + tid + ':snaps'))

        if results['result'].lower() == 'pass':
            if snapshots is not None:
                for d in snapshots:
                    if 'fid' in d:
                        self.deletefile(d['fid'])
            snapshots = []

        self._db[
            'testresults'].update({'gid': gid, 'sid': sid, 'tid': int(tid)},
                                  {'$set': {'result': results['result'].lower(),
                                            'traceinfo': results['traceinfo'],
                                            'endtime': results['time'],
                                            'snapshots': snapshots}})

    def writeTestLog(self, gid, sid, tid, logfile):
        """
        add log file in GridFS
        update the corresponding test case resut record
        """
        caseresult = self._db['testresults']
        fkey = self.setfile(logfile)
        caseresult.update({'gid': gid, 'sid': sid, 'tid': int(
            tid)}, {'$set': {'log': fkey}})

    def writeTestSnapshot(self, gid, sid, tid, snapfile, stype):
        """
        add snapshot png in image buffer
        """
        snaps = self.getCache(str('sid:' + sid + ':tid:' + tid + ':snaps'))
        if snaps is None:
            snaps = []
        try:
            values = stype.split(':')
            xtype, sfile = values[0], values[1]
            results = self._db['testresults']
            fkey = self.setfile(snapfile)
            snapfile.seek(0)
            if xtype == 'expect':
                results.update({'gid': gid, 'sid': sid, 'tid': int(tid)},
                               {'$set': {'checksnap': {'title': sfile, 'fid': fkey}}})
            elif xtype == 'current':
                snaps.append({'title': sfile, 'fid': fkey})
                timenow = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                self.setCache(str('sid:' + sid + ':snap'), snapfile.read())
                self.setCache(str('sid:' + sid + ':snaptime'), timenow)
                self.setCache(str('sid:' + sid + ':tid:' + tid + ':snaps'), snaps)
        except:
            pass

    def readTestLiveSnaps(self, gid, sid, timestamp):
        result = None
        snaptime = self.getCache(str('sid:' + sid + ':snaptime'))
        if snaptime is not None and timestamp != snaptime:
            snap = self.getCache(str('sid:' + sid + ':snap'))
            result = {'snap': snap, 'snaptime': snaptime}
        return result

    def getCaseLog(self, fid):
        """
        read list of test session records in database
        """
        data = self.getfile(fid)
        if not data is None:
            return data
        else:
            return None

    def readTestCaseSnap(self, fid):
        data = self.getfile(fid)
        if not data is None:
            return data
        else:
            return None

    def readTestHistorySnaps(self, gid, sid, tid):
        caseresult = self._db['testresults']
        ret = caseresult.find_one({'sid': sid, 'tid': int(tid)})
        snapids = []
        snaps = []
        checkid = ''
        checksnap = ''
        stitle = ''
        if ret is not None:
            snapids = ret['snapshots']
            if not 'checksnap' in ret:
                checksnap = {'title': '', 'url': ''}
            else:
                stitle = ret['checksnap']['title']
                checkid = ret['checksnap']['fid']
                checksnap = {'title': stitle, 'url': checkid}

        if not snapids is None:
            for d in snapids:
                stitle = d['title']
                fid = d['fid']
                snaps.append({'title': stitle, 'url': fid})

        return {'snaps': snaps, 'checksnap': checksnap}


def __getStore():
    mongo_uri = MONGODB_URI
    replicaset = MONGODB_REPLICASET
    mongo_client = MONGODB_REPLICASET and MongoReplicaSetClient(
        mongo_uri, replicaSet=replicaset, read_preference=ReadPreference.PRIMARY) or MongoClient(mongo_uri)
    mem = memcache.Client(MEMCACHED_URI.split(','))
    return DataStore(mongo_client, mem)

store = __getStore()
