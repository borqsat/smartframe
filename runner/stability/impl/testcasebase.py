import sys,os,time
import unittest
import uuid
from builder import TestBuilder
from stability.util.log import Logger
from testworker import testWorker

class TestCaseBase(unittest.TestCase):

    def setUp(self):
        super(TestCaseBase, self).setUp()
        self.tid = str(uuid.uuid1()) 
        self.starttime = time.strftime('%Y.%m.%d-%H.%M.%S', time.localtime(time.time()))
        self.worker = testWorker(TestBuilder.getBuilder(), self)
        self.logger = Logger.getLogger()

    def tearDown(self):
        super(TestCaseBase, self).tearDown()     
        
