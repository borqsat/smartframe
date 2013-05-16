import unittest
import os
import sys
from bson.objectid import ObjectId
from datetime import datetime
from datetime import timedelta

from pymongo import MongoClient
import gridfs

DIRNAME = os.path.abspath(os.path.dirname(__file__))

from smartserver.v0.impl.dbstore import store

class TestDelete(unittest.TestCase):
	'''
	Test for group, session delete and dirty clear. Should setup mongodb.
	'''
	def setUp(self):
		self.orig_argv = sys.argv
		sys.argv = self.orig_argv[0:1]
		self._mc = MongoClient("mongodb://localhost:27017")
		self._db_server = self._mc.smartServer
		self._db_fs = self._mc.smartFiles

		self._fs = gridfs.GridFS(self._db_fs, collection="fs")

		self._c_results = self._db_server['testresults']
		self._c_sessions = self._db_server['testsessions']
		self._c_groups = self._db_server['groups']
		self._c_fs = self._db_fs['fs.files']

		#Prepare test data. First, empty database, and insert the test data including files. 
		self._c_results.remove()
		self._c_sessions.remove()
		self._c_groups.remove()
		self._c_fs.remove()

		#Insert 4 files, 3 of which is used in log, snapshot and checksnap, and the other one is
		# dirty file. 
		self._f_log = str(self._fs.put('log_data'))
		self._f_check = str(self._fs.put('check_data'))
		self._f_snap = str(self._fs.put('snap_data'))
		self._f_tmp = str(self._fs.put('tmp_data'))
		self._c_fs.update({'_id': ObjectId(self._f_log)}, {'$set':{'uploadDate':datetime.now()-timedelta(3)}})
		self._c_fs.update({'_id': ObjectId(self._f_check)}, {'$set':{'uploadDate':datetime.now()-timedelta(3)}})
		self._c_fs.update({'_id': ObjectId(self._f_snap)}, {'$set':{'uploadDate':datetime.now()-timedelta(3)}})
		self._c_fs.update({'_id': ObjectId(self._f_tmp)}, {'$set':{'uploadDate':datetime.now()-timedelta(3)}})

		#Insert 1 group
		self._c_groups.insert({'gid': 'g001', 'groupname': 'groupname', 'info': 'info'})

		#Insert 2 sessions, 1 for the existed group, and the other's group has been deleted
		self._c_sessions.insert({'id': 1, 'gid': 'g001', 'sid': 's001',
						'tester': 'tester', 'planname': 'planname',
						'starttime': 'starttime', 'endtime': 'endtime', 'runtime': 0,
						'summary': {'total': 0, 'pass': 0, 'fail': 0, 'error': 0},
						'deviceid': 'deviceid', 'deviceinfo': 'devinfo'})

		self._c_sessions.insert({'id': 2, 'gid': 'g002', 'sid': 's002',
						'tester': 'tester', 'planname': 'planname',
						'starttime': 'starttime', 'endtime': 'endtime', 'runtime': 0,
						'summary': {'total': 0, 'pass': 0, 'fail': 0, 'error': 0},
						'deviceid': 'deviceid', 'deviceinfo': 'devinfo'})

		#Insert 2 test result, 1 for the existed test session, and the other's session have been deleted.
		self._c_results.insert({'gid': 'g001', 'sid': 's001', 'tid': 1,
						'casename': 'casename', 'log': self._f_log, 'starttime': 'starttime', 'endtime': 'endtime',
						'traceinfo':'N/A', 'result': 'fail',  'snapshots': [{'fid': self._f_snap, 'tile': 'snap'}],
						'checksnap' : { "fid" : self._f_check, "title" : "None" }
						})

		self._c_results.insert({'gid': 'g002', 'sid': 's002', 'tid': 1,
						'casename': 'casename', 'log': 'N/A', 'starttime': 'starttime', 'endtime': 'endtime',
						'traceinfo':'N/A', 'result': 'pass',  'snapshots': []})


	def tearDown(self):
		#self._c_results.remove()
		#self._c_sessions.remove()
		#self._c_groups.remove()
		#self._c_fs.remove()
		sys.argv = self.orig_argv

	def testDeleteGroup(self):
		'''
		Only delete all test sessions, test results and files according to the group id. 
		'''
		store.del_group('g001')
		self.assertEqual(self._c_sessions.find({'gid': 'g001'}).count(), 0)
		self.assertEqual(self._c_sessions.find({'gid': 'g002'}).count(), 1)
		self.assertEqual(self._c_results.find({'gid': 'g001'}).count(), 0)
		self.assertEqual(self._c_results.find({'gid': 'g002'}).count(), 1)
		self.assertEqual(self._c_fs.find({'_id':ObjectId(self._f_log)}).count(), 0)
		self.assertEqual(self._c_fs.find({'_id':ObjectId(self._f_check)}).count(), 0)
		self.assertEqual(self._c_fs.find({'_id':ObjectId(self._f_snap)}).count(), 0)
		self.assertEqual(self._c_fs.find({'_id':ObjectId(self._f_tmp)}).count(), 1)

	def testDeleteSession(self):
		'''
		Only delete all test results and fs according to the session id. 
		'''
		store.del_session('s001')
		self.assertEqual(self._c_results.find({'sid': 's001'}).count(), 0)
		self.assertEqual(self._c_results.find({'sid': 's002'}).count(), 1)
		self.assertEqual(self._c_fs.find({'_id':ObjectId(self._f_log)}).count(), 0)
		self.assertEqual(self._c_fs.find({'_id':ObjectId(self._f_check)}).count(), 0)
		self.assertEqual(self._c_fs.find({'_id':ObjectId(self._f_snap)}).count(), 0)
		self.assertEqual(self._c_fs.find({'_id':ObjectId(self._f_tmp)}).count(), 1)


	def testDeleteDirty(self):
		'''
		Only dirty data will be deleted, like the sessions which gid is not exist, the test result
		which session is not exist and the files which is not used in testresults' log, snapshot and 
		checksnap. 

		The function 
		'''
		store.del_dirty()
		self.assertEqual(self._c_sessions.find({'gid': 'g001'}).count(), 1)
		self.assertEqual(self._c_sessions.find({'gid': 'g002'}).count(), 0)
		self.assertEqual(self._c_results.find({'gid': 'g001'}).count(), 1)
		self.assertEqual(self._c_results.find({'gid': 'g002'}).count(), 0)
		self.assertEqual(self._c_fs.find({'_id':ObjectId(self._f_log)}).count(), 1)
		self.assertEqual(self._c_fs.find({'_id':ObjectId(self._f_check)}).count(), 1)
		self.assertEqual(self._c_fs.find({'_id':ObjectId(self._f_snap)}).count(), 1)
		self.assertEqual(self._c_fs.find({'_id':ObjectId(self._f_tmp)}).count(), 0)

	def testCheck_fs(self):
		r = store.check_fs(self._f_log)
		self.assertEqual(r[0], True)
		self.assertEqual(r[1], False)
		self.assertEqual(r[2], False)
		r = store.check_fs(self._f_snap)
		self.assertEqual(r[0], False)
		self.assertEqual(r[1], True)
		self.assertEqual(r[2], False)
		r = store.check_fs(self._f_check)
		self.assertEqual(r[0], False)
		self.assertEqual(r[1], False)
		self.assertEqual(r[2], True)
		r = store.check_fs(self._f_tmp)
		self.assertEqual(r[0], False)
		self.assertEqual(r[1], False)
		self.assertEqual(r[2], False)
