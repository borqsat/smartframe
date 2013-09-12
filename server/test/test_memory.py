import unittest
import os
import sys
from bson.objectid import ObjectId
from datetime import datetime
from datetime import timedelta

from pymongo import MongoClient
import gridfs

from smartserver.v0.impl.dbstore import store

DIRNAME = os.path.abspath(os.path.dirname(__file__))

class TestMemory(unittest.TestCase):
	'''
	Test for  Should setup mongodb.
	'''
	def setUp(self):
		self.orig_argv = sys.argv
		sys.argv = self.orig_argv[0:1]
		from smartserver.v0 import config
		_config = reload(config)
		self._mc = MongoClient(_config.MONGODB_URI)
		self._db_server = self._mc.smartServer

		self._c_memory = self._db_server['testdeviceMemory']
		self._c_processlist = self._db_server['testprocesslist']


		#Prepare test data. First, empty database, and insert the test data including files. 
		self._c_memory.remove()
		self._c_processlist.remove()
		self._c_memory.insert({'id': 2, 'gid': 'g002', 'sid': 's002','date': '20130907','cpu': {'com_tencent_mobileqq': 1,'cpuset': 3},'memory': 473144,'process': {'system_server':45344,'com_android_systemui': 28772,'com_tencent_mobileqq': 22468}})
		self._c_memory.insert({'id': 2, 'gid': 'g002', 'sid': 's002',
						'date':'201309010','cpu':{'com_tencent_mobileqq':1,'cpuset':3},
						'memory':473148,'process':{'system_server':45344,'com_android_systemui':28772,'com_tencent_mobileqq':22468}})


	def tearDown(self):
		self._c_memory.remove()
		self._c_processlist.remove()
		sys.argv = self.orig_argv

	def testGetMemory(self):
		result = store.getDeviceMemory(gid='g002',sid='s002',value={'cpu':['cpuset','com_tencent_mobileqq'],'memory':1,'process':['system_server','com_android_systemui']})
		self.assertEqual(result['date'][0], '20130907')
		self.assertEqual(result['date'][1], '201309010')
		self.assertEqual(result['dataset']['memory'][0], 473144)
		self.assertEqual(result['dataset']['process,system_server'][0], 45344)

	def testProcessList(self):
		store.updateDeviceMemory(gid='g002',sid='s002',value = {'date':'20130902','cpu':{'com_tencent_mobileqq': 1,'cpuset': 3},'memory':473144,'process':{'system_server':45344,'com_android_systemui':28772}})
		result = store.getMemoryList(gid='g002',sid='s002')
		self.assertEqual(result['cpu'][0], 'cpuset')
		self.assertEqual(result['process'][0], 'system_server')